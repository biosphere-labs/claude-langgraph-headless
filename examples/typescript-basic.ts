/**
 * Basic usage example - TypeScript
 */

import { ClaudeHeadlessExecutor, ClaudeHeadlessNode } from "../src/index";

async function basicExample() {
  console.log("=== Basic Claude Headless Example ===\n");

  // Create executor
  const executor = new ClaudeHeadlessExecutor({
    outputFormat: "json",
    timeout: 60000,
    useSubscription: true,
  });

  // Execute
  const result = await executor.execute({
    systemPrompt: "You are a helpful assistant that analyzes conversations.",
    userPrompt: "What are the top 3 reasons conversations fail?",
  });

  console.log("Result:", result.result);
  console.log("Exit code:", result.exitCode);
}

async function langGraphNodeExample() {
  console.log("\n=== LangGraph Node Example ===\n");

  // Create a LangGraph-compatible node
  const claudeNode = new ClaudeHeadlessNode({
    outputFormat: "json",
    timeout: 60000,
  });

  // Use in your LangGraph workflow
  const result = await claudeNode.invoke({
    systemPrompt: "You are an expert at identifying missing context.",
    userPrompt: "Analyze this conversation and identify what information was missing...",
  });

  console.log("Node result:", result);
}

// Run examples
(async () => {
  try {
    await basicExample();
    await langGraphNodeExample();
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
})();
