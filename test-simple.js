/**
 * Simple test to verify the package works
 */

const { ClaudeHeadlessNode } = require('./dist/index');

async function test() {
  console.log('Testing Claude Headless Node...\n');

  const node = new ClaudeHeadlessNode({
    outputFormat: 'text',
    timeout: 60000,
    useSubscription: true,
  });

  try {
    const result = await node.invoke({
      systemPrompt: 'You are a helpful assistant. Respond with only "WORKING".',
      userPrompt: 'Test message - respond with WORKING',
    });

    console.log('✅ Success!');
    console.log('Result:', result.result);
    console.log('Exit code:', result.exitCode);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

test();
