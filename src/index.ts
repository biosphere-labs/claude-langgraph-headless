import { spawn, ChildProcess } from "child_process";
import { writeFileSync, unlinkSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";

export interface ClaudeHeadlessOptions {
  outputFormat?: "text" | "json" | "stream-json";
  timeout?: number; // milliseconds
  maxBuffer?: number; // bytes
  useSubscription?: boolean; // Use subscription instead of API billing
  retries?: number;
}

export interface ClaudeHeadlessInput {
  systemPrompt: string;
  userPrompt: string;
}

export interface ClaudeHeadlessOutput {
  result: string;
  error?: string;
  exitCode?: number;
}

/**
 * Robust Claude Code headless executor using spawn for better process control
 */
export class ClaudeHeadlessExecutor {
  private options: Required<ClaudeHeadlessOptions>;

  constructor(options: ClaudeHeadlessOptions = {}) {
    this.options = {
      outputFormat: options.outputFormat || "json",
      timeout: options.timeout || 180000, // 3 minutes
      maxBuffer: options.maxBuffer || 10 * 1024 * 1024, // 10MB
      useSubscription: options.useSubscription !== false, // Default true
      retries: options.retries || 0,
    };
  }

  /**
   * Execute Claude Code in headless mode
   */
  async execute(input: ClaudeHeadlessInput): Promise<ClaudeHeadlessOutput> {
    let attempt = 0;
    let lastError: Error | null = null;

    while (attempt <= this.options.retries) {
      try {
        return await this._executeOnce(input);
      } catch (error) {
        lastError = error as Error;
        attempt++;
        if (attempt <= this.options.retries) {
          console.warn(`Attempt ${attempt} failed, retrying...`);
          await this._delay(1000 * attempt); // Exponential backoff
        }
      }
    }

    throw lastError || new Error("Execution failed");
  }

  private async _executeOnce(
    input: ClaudeHeadlessInput
  ): Promise<ClaudeHeadlessOutput> {
    const tempFile = join(tmpdir(), `claude-prompt-${Date.now()}-${Math.random().toString(36).substr(2, 9)}.txt`);
    const fullPrompt = `${input.systemPrompt}\n\n---\n\n${input.userPrompt}`;

    try {
      // Write prompt to temp file
      writeFileSync(tempFile, fullPrompt, "utf-8");

      // Execute using spawn for better control
      const result = await this._spawnClaudeProcess(tempFile);

      // Clean up
      unlinkSync(tempFile);

      return result;
    } catch (error) {
      // Clean up temp file on error
      try {
        unlinkSync(tempFile);
      } catch {}

      throw error;
    }
  }

  private _spawnClaudeProcess(
    tempFile: string
  ): Promise<ClaudeHeadlessOutput> {
    return new Promise((resolve, reject) => {
      // Use interactive mode with -p and --settings to use subscription
      const settingsFlag = {
        env: {
          // Force subscription mode by clearing API key
          ANTHROPIC_API_KEY: "",
        }
      };

      const args = [
        "-p",
        "--output-format", this.options.outputFormat,
        "--settings", JSON.stringify(settingsFlag)
      ];

      // Set up environment - unset API key if using subscription
      const env = { ...process.env };
      if (this.options.useSubscription) {
        delete env.ANTHROPIC_API_KEY;
      }

      // Spawn claude process
      const claude: ChildProcess = spawn("claude", args, {
        env,
        stdio: ["pipe", "pipe", "pipe"],
      });

      let stdout = "";
      let stderr = "";
      let stdoutSize = 0;
      let timedOut = false;

      // Set timeout
      const timeoutHandle = setTimeout(() => {
        timedOut = true;
        claude.kill("SIGTERM");

        // Force kill if still running after 5s
        setTimeout(() => {
          if (!claude.killed) {
            claude.kill("SIGKILL");
          }
        }, 5000);
      }, this.options.timeout);

      // Handle stdout
      claude.stdout?.on("data", (data: Buffer) => {
        stdoutSize += data.length;
        if (stdoutSize > this.options.maxBuffer) {
          claude.kill("SIGTERM");
          clearTimeout(timeoutHandle);
          reject(
            new Error(
              `Output exceeded max buffer size of ${this.options.maxBuffer} bytes`
            )
          );
          return;
        }
        stdout += data.toString();
      });

      // Handle stderr
      claude.stderr?.on("data", (data: Buffer) => {
        stderr += data.toString();
      });

      // Handle process exit
      claude.on("close", (code: number | null, signal: string | null) => {
        clearTimeout(timeoutHandle);

        if (timedOut) {
          reject(
            new Error(
              `Claude process timed out after ${this.options.timeout}ms`
            )
          );
          return;
        }

        if (signal) {
          reject(new Error(`Claude process killed by signal: ${signal}`));
          return;
        }

        // Check for credit balance error in JSON output
        if (stdout.includes('"result":"Credit balance is too low"')) {
          reject(
            new Error(
              "Credit balance is too low. Use subscription authentication or add API credits."
            )
          );
          return;
        }

        if (code !== 0) {
          reject(
            new Error(
              `Claude process exited with code ${code}\nStderr: ${stderr}\nStdout: ${stdout}`
            )
          );
          return;
        }

        resolve({
          result: stdout.trim(),
          exitCode: code || 0,
        });
      });

      // Handle spawn errors
      claude.on("error", (error: Error) => {
        clearTimeout(timeoutHandle);
        reject(new Error(`Failed to spawn claude process: ${error.message}`));
      });

      // Pipe prompt from temp file to stdin
      const cat = spawn("cat", [tempFile]);
      cat.stdout?.pipe(claude.stdin!);
      cat.on("error", (error) => {
        clearTimeout(timeoutHandle);
        claude.kill();
        reject(new Error(`Failed to read prompt file: ${error.message}`));
      });
    });
  }

  private _delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

/**
 * LangGraph-compatible node for Claude Code headless execution
 */
export class ClaudeHeadlessNode {
  private executor: ClaudeHeadlessExecutor;

  constructor(options: ClaudeHeadlessOptions = {}) {
    this.executor = new ClaudeHeadlessExecutor(options);
  }

  /**
   * LangGraph node invoke method
   */
  async invoke(input: ClaudeHeadlessInput): Promise<ClaudeHeadlessOutput> {
    return this.executor.execute(input);
  }
}

// Types are already exported above via interface declarations
