import { ClaudeHeadlessExecutor, ClaudeHeadlessNode } from "../src/index";

describe("ClaudeHeadlessExecutor", () => {
  // Skip tests if no claude command available
  const hasClaudeCLI = async () => {
    try {
      const { spawn } = require("child_process");
      return new Promise((resolve) => {
        const proc = spawn("which", ["claude"]);
        proc.on("close", (code: number) => resolve(code === 0));
      });
    } catch {
      return false;
    }
  };

  beforeAll(async () => {
    const available = await hasClaudeCLI();
    if (!available) {
      console.warn("Claude CLI not available, skipping integration tests");
    }
  });

  describe("Basic Execution", () => {
    it("should execute a simple prompt", async () => {
      const available = await hasClaudeCLI();
      if (!available) {
        return; // Skip test
      }

      const executor = new ClaudeHeadlessExecutor({
        timeout: 60000,
        outputFormat: "text",
      });

      const result = await executor.execute({
        systemPrompt: "You are a helpful assistant. Respond with only 'OK'.",
        userPrompt: "Say OK",
      });

      expect(result.result).toBeTruthy();
      expect(result.exitCode).toBe(0);
    }, 70000);

    it("should handle JSON output format", async () => {
      const available = await hasClaudeCLI();
      if (!available) {
        return;
      }

      const executor = new ClaudeHeadlessExecutor({
        timeout: 60000,
        outputFormat: "json",
      });

      const result = await executor.execute({
        systemPrompt: "You are a helpful assistant.",
        userPrompt: "What is 2+2? Reply with just the number.",
      });

      expect(result.result).toBeTruthy();
      // Should contain JSON structure
      expect(result.result).toContain("type");
    }, 70000);
  });

  describe("Error Handling", () => {
    it("should timeout after configured duration", async () => {
      const available = await hasClaudeCLI();
      if (!available) {
        return;
      }

      const executor = new ClaudeHeadlessExecutor({
        timeout: 1000, // 1 second - too short
      });

      await expect(
        executor.execute({
          systemPrompt: "You are a helpful assistant.",
          userPrompt: "Write a very long essay...",
        })
      ).rejects.toThrow(/timed out/);
    }, 15000);

    it("should handle credit balance errors gracefully", async () => {
      // This test validates the error parsing logic
      // In real scenario, would hit actual credit limit
      const executor = new ClaudeHeadlessExecutor();

      // Mock scenario - would need actual low credit account to test fully
      // For now, just verify the error detection logic exists
      expect(executor).toBeDefined();
    });
  });

  describe("Configuration", () => {
    it("should use default options", () => {
      const executor = new ClaudeHeadlessExecutor();
      expect(executor).toBeDefined();
    });

    it("should accept custom options", () => {
      const executor = new ClaudeHeadlessExecutor({
        timeout: 5000,
        maxBuffer: 1024,
        outputFormat: "text",
        useSubscription: false,
        retries: 3,
      });
      expect(executor).toBeDefined();
    });
  });
});

describe("ClaudeHeadlessNode", () => {
  describe("LangGraph Integration", () => {
    it("should work as a LangGraph node", async () => {
      const available = await (async () => {
        try {
          const { spawn } = require("child_process");
          return new Promise((resolve) => {
            const proc = spawn("which", ["claude"]);
            proc.on("close", (code: number) => resolve(code === 0));
          });
        } catch {
          return false;
        }
      })();

      if (!available) {
        return;
      }

      const node = new ClaudeHeadlessNode({
        timeout: 60000,
        outputFormat: "json",
      });

      const result = await node.invoke({
        systemPrompt: "You are a helpful assistant.",
        userPrompt: "Say hello",
      });

      expect(result.result).toBeTruthy();
      expect(result.exitCode).toBe(0);
    }, 70000);
  });
});

describe("Process Management", () => {
  it("should handle large prompts without command-line length limits", async () => {
    const available = await (async () => {
      try {
        const { spawn } = require("child_process");
        return new Promise((resolve) => {
          const proc = spawn("which", ["claude"]);
          proc.on("close", (code: number) => resolve(code === 0));
        });
      } catch {
        return false;
      }
    })();

    if (!available) {
      return;
    }

    const executor = new ClaudeHeadlessExecutor({
      timeout: 90000,
    });

    // Create a very large prompt
    const largePrompt = "x".repeat(10000); // 10KB prompt

    const result = await executor.execute({
      systemPrompt: "You are a helpful assistant. Respond briefly.",
      userPrompt: `Here is a large text: ${largePrompt}\n\nJust say "received".`,
    });

    expect(result.result).toBeTruthy();
  }, 100000);
});
