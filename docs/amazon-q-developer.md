# Amazon Q Developer 🚀

![AWS](https://img.shields.io/badge/AWS-Bedrock-orange?logo=amazon-aws) ![IDE](https://img.shields.io/badge/IDE-Assistant-blue) ![AI](https://img.shields.io/badge/AI-Coding_Assistant-purple)

Amazon Q Developer is an AI-powered coding assistant that helps you write, understand, and modernize applications—especially on AWS. It combines advanced language models with deep AWS expertise to provide real-time suggestions, automated analysis, and interactive help right in your IDE.

> 🎯 Goal: Use Q Developer to speed up development, improve code quality, and adopt AWS best practices.

---

## Table of contents
- Core features and capabilities
- Practical example: Serverless data processing
- Practical example: Code modernization
- Common use cases
- Amazon Q Detector Library

---

## Core features and capabilities

### Intelligent chat interface 💬
Use a Bedrock-powered conversational interface to:
- Ask technical questions about AWS services and best practices
- Request code explanations and documentation
- Generate code solutions for specific tasks
- Debug and troubleshoot issues in real time

### Code generation and enhancement 🧠
Backed by large language models (and AWS know-how), Q Developer offers:
- Context-aware code suggestions as you type
- Complete function and application scaffolding
- AWS service integration templates
- Code optimization recommendations
- Security vulnerability detection and remediation

### Specialized AI agents 🤖
Invoke task-specific agents directly from chat: `/dev`, `/test`, `/review`, `/transform`, `/doc`

- Development Agent
  - Assists with code writing and refactoring
  - Optimizes code performance
  - Implements AWS best practices

- Testing Agent
  - Generates comprehensive test cases
  - Identifies edge cases
  - Improves test coverage
  - Validates code functionality

- Review Agent
  - Performs automated code reviews
  - Enforces coding standards
  - Suggests architectural improvements
  - Identifies potential issues

- Transform Agent
  - Facilitates code migration
  - Updates legacy codebases
  - Converts between frameworks
  - Modernizes applications

- Documentation Agent
  - Creates clear, comprehensive documentation
  - Generates API references and usage guides
  - Maintains documentation accuracy

## Quick start ⚡️

- Open Q Developer chat in your IDE
- Try slash-commands for agents:
  - `/dev` (development), `/test` (testing), `/review` (reviews), `/transform` (modernization), `/doc` (documentation)
- Example prompts:
  - “Create a Python Lambda that reads from SQS and writes to DynamoDB.”
  - “Explain this CloudFormation template and suggest security improvements.”
  - “Refactor this function to improve readability and performance.”

---

## Practical example: Serverless data processing ⚡️

Task: Create a Lambda function to process SQS messages and store data in DynamoDB.

Just ask in Q Developer chat:

> Create a Python Lambda function that processes messages from an SQS queue and stores the data in DynamoDB

Q Developer typically generates a complete solution, including:
- Function structure
- AWS SDK integration
- Error handling
- Logging
- Best practices implementation

## Practical example: Code modernization 🔄

Scenario: Upgrade a Java application from version 8 to 17.

Ask in chat:

> Help me upgrade this Java 8 application to Java 17. Here are the key files...

Q Developer will:
1. Analyze your codebase
2. Identify deprecated features
3. Suggest modern replacements
4. Guide you through breaking changes

Examples of suggestions:
- Update Collections code to use Stream APIs
- Replace legacy Date/Calendar code with `java.time`
- Modernize try-catch with try-with-resources

Q Developer breaks down complex migration tasks into manageable steps, explains the changes, and helps you implement them correctly. This same approach works for many modernization tasks, from framework upgrades to adopting new AWS services.

---

## Common use cases 🧰
- Writing new AWS applications
- Debugging existing code
- Learning AWS services
- Implementing security best practices
- Generating documentation
- Modernizing applications

Whether you’re building serverless apps, working with AWS services, or maintaining existing code, Amazon Q Developer can streamline your development process and boost productivity. As you progress through this course, keep exploring how AI-assisted development can help you move faster with confidence. 

> 🧭 This repository is for learning and preparing for the Amazon GenAI Developer Professional certification—use Q Developer to explore patterns and reinforce concepts as you go.

---

## Amazon Q Detector Library 🛡️

The Amazon Q Detector Library describes the detectors used during code reviews to identify security and quality issues in code. Detectors contain rules to surface critical vulnerabilities (OWASP Top 10, CWE Top 25), secrets exposure, dependency risks, and code quality concerns (e.g., IaC best practices, inefficient AWS API usage). Use Amazon Q Developer code reviews (and Amazon Inspector code scanning for Lambda) to receive intelligent findings and remediation guidance.

**Key points**
- ✅ Detects security and quality issues with curated rules and severities
- 🕵️ Secrets exposure, dependency vulnerabilities, insecure cryptography, and more
- 🧭 Surfaces AWS best-practice guidance and inefficient usage patterns
- 🧪 Complements Amazon Q code reviews and Amazon Inspector code scanning

**Change log**
- 📒 A history of detector additions and improvements is published to the Amazon Q Detector Library change log.

### Detector Library highlights ✅

- What it is: A reference for Amazon Q’s security and code-quality detectors, with severities, CWE refs, and compliant/noncompliant examples
- How to use: Study detector behavior and remediation guidance; after running code reviews, use pages to mitigate findings and align to AWS best practices
- Try it: Use the Amazon Q example detection repository with Amazon Q code reviews or Amazon Inspector code scanning to see findings in action
- Updates: Detectors are continuously added/updated to cover new vulnerability classes and quality issues
- Coverage breadth: Detectors match classes of defects, not just the specific example shown on a page
- Availability: Q code reviews include hundreds of security and quality detectors (language support varies). Amazon Inspector code scanning applies these to Lambda (see service docs for supported languages)
- Smart scoping: Q filters out unsupported languages, test code, and open-source code to focus on relevant customer code


