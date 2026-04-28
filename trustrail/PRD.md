# TrustRail Product Requirements Document (PRD)

## Project Vision

TrustRail is a high-performance Shift-Left Security ecosystem designed to prevent sensitive data leaks before they reach the repository. By integrating seamlessly into developer workflows, TrustRail enables early detection and remediation of secrets in code, ensuring compliance with security best practices without compromising productivity. As a local-first solution, it prioritizes privacy while providing optional cloud-based telemetry for organizational insights.

## Detailed Feature Set

### Modular Scanner (Regex + Entropy)
- **Core Functionality**: A Python-based scanning engine that analyzes source code for sensitive data using a combination of regular expressions and entropy analysis.
- **Modularity**: Pluggable detector architecture allowing easy addition of new secret types.
- **Performance**: Optimized for real-time scanning with minimal IDE impact through event-driven triggers and debouncing.
- **Accuracy**: High precision detection with configurable thresholds to minimize false positives.

### Git Gatekeeper (Pre-Commit Hook)
- **Integration**: Automated pre-commit hook that scans staged files for secrets.
- **Blocking Mechanism**: Prevents commits containing detected secrets, providing clear error messages and remediation guidance.
- **User Experience**: Non-intrusive installation and optional bypass for emergency commits.

### Cloud Telemetry (Django Dashboard)
- **Incident Logging**: Anonymous logging of detection events for trend analysis and compliance reporting.
- **Dashboard**: Web-based interface for viewing aggregated telemetry data, including secret types, frequencies, and user anonymized metrics.
- **Opt-In Basis**: Telemetry is disabled by default, with explicit user consent required for data transmission.

### Prompt Injection Defense
- **API Proxy Layer**: Intercepts and scans LLM prompts for jailbreak attempts, preventing malicious inputs from compromising AI models.
- **Real-Time Analysis**: Automated detection of common jailbreak patterns and injection vectors.

### LSP-based Scanning
- **Language Server Protocol Integration**: Asynchronous, non-blocking IDE integration for real-time scanning without disrupting developer workflow.
- **Cross-IDE Support**: Compatible with VS Code, IntelliJ, and other LSP-enabled editors.

### Smart Triggers
- **Optimized Scanning**: Implements 3-5s debounce or on-save triggers to balance security with CPU/battery efficiency.
- **Adaptive Logic**: Adjusts scanning frequency based on file changes and user activity.

### AI-Powered Verification
- **Local Micro-AI Model**: Uses lightweight AI to verify high-entropy strings, significantly reducing false positives.
- **Machine Learning Enhancement**: Trained on secret patterns to improve detection accuracy over time.

### Audit Logs
- **Immutable Logging**: Generates tamper-proof logs for ISO27001/SOC2 compliance tracking.
- **Comprehensive Tracking**: Records detection events, remediation actions, and user interactions for audit purposes.

## Expanded Detection Scope

TrustRail supports comprehensive detection across multiple categories:

- **Cloud Providers**:
  - AWS: Access Keys, Secret Keys, Session Tokens.
  - GCP: Service Account Keys, API Keys.
  - Azure: Access Tokens, Client Secrets.

- **AI/ML Platforms**:
  - OpenAI: API Keys (e.g., sk-* patterns).
  - Anthropic: API Keys (e.g., sk-ant-*).
  - HuggingFace: API Tokens.
  - LangChain: Integration Keys.

- **DevOps & Infrastructure**:
  - GitHub: Personal Access Tokens (ghp_*).
  - SSH Keys: Private Key detection.
  - Docker: Configs and Registry Tokens.

- **Payments & Databases**:
  - Stripe: Secret Keys (sk_test_*, rk_live_*).
  - PostgreSQL: Connection Strings.
  - Redis: Connection URLs.

Detection leverages both regex patterns and entropy analysis to identify high-entropy strings indicative of secrets.

## Technical Architecture

### Backend
- **Framework**: Django with Django REST Framework (DRF) for API development.
- **Database**: PostgreSQL for production, SQLite for development.
- **API Endpoints**: RESTful APIs for telemetry ingestion and dashboard data retrieval.
- **Security**: Rate limiting, authentication, and data encryption for telemetry data.

### Frontend
- **Framework**: React.js with TypeScript for type safety.
- **Components**: Dashboard for telemetry visualization, configuration panels for scanner settings.
- **Integration**: API calls to Django backend for real-time data.
- **Deployment**: Static hosting with CDN for performance.

### CLI Tool
- **Language**: Python with Click or Argparse for command-line interface.
- **Commands**: Scan directories, apply fixes, install hooks, configure telemetry.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.

### Overall Architecture
- **Local-First Design**: All scanning occurs on the developer's machine; no raw code is transmitted.
- **Event-Driven**: Integrates with IDEs via plugins (future) for on-save scanning.
- **Scalability**: Modular architecture supports horizontal scaling for enterprise deployments.

## Privacy Constraints

TrustRail adheres to a strict "Local-First" policy to protect user privacy:

- **Data Flow**: Raw source code never leaves the developer's machine. Scanning and remediation are performed locally.
- **Telemetry**: Only anonymized metadata is optionally sent to the cloud, including:
  - `user_hash`: SHA-256 hash of a unique user identifier (e.g., machine ID or user-provided ID).
  - `secret_type`: Categorization of detected secret (e.g., "aws_access_key").
  - `file_name`: Relative path to the file containing the secret (no content).
- **Anonymization**: No personally identifiable information (PII) or sensitive data is collected without explicit consent.
- **Compliance**: Designed to meet GDPR, CCPA, and similar regulations by defaulting to opt-out and providing clear data handling policies.
- **Encryption**: All telemetry data is transmitted over HTTPS and stored encrypted.

## Phased Roadmap

### Phase 1: Core Logic (Scanner and Detectors)
- **Duration**: 2-4 weeks.
- **Deliverables**: Functional scanner engine with detectors for all specified categories, CLI tool for local scanning.
- **Milestones**: Unit tests for detectors, integration tests for scanner, performance benchmarks.
- **Risks**: Regex false positives; mitigation via entropy thresholds and allowlists.

### Phase 2: Git Integration and Remediation
- **Duration**: 2-3 weeks.
- **Deliverables**: Pre-commit hook implementation, Quick Fix automation for .env relocation.
- **Milestones**: Hook installation scripts, remediation testing, Git workflow integration.
- **Risks**: Hook conflicts with existing setups; mitigation via user confirmation and rollback options.

### Phase 3: Backend and Telemetry
- **Duration**: 3-4 weeks.
- **Deliverables**: Django backend with DRF APIs, telemetry client, database schema.
- **Milestones**: API endpoint testing, anonymization validation, security audits.
- **Risks**: Data privacy breaches; mitigation via code reviews and penetration testing.

### Phase 4: UI Demo (React Dashboard)
- **Duration**: 2-3 weeks.
- **Deliverables**: React frontend for dashboard, end-to-end telemetry flow demonstration.
- **Milestones**: UI/UX design, API integration, demo deployment.
- **Risks**: Frontend-backend sync issues; mitigation via API versioning and testing.

## Success Metrics
- **Detection Accuracy**: >95% true positives with <5% false positives.
- **Performance**: Scanning completes in <1 second for typical codebases.
- **Adoption**: Successful integration in at least 3 pilot projects.
- **Privacy Compliance**: Zero reported privacy incidents.

## Assumptions and Dependencies
- Target users have Python 3.8+ and Git installed.
- Enterprise deployments may require on-premise backend hosting.
- Open-source contributions for additional detectors.

## Open Questions
- Specific IDE integrations (e.g., VS Code plugin)?
- Multi-language support beyond Python?
- Integration with CI/CD pipelines?

This PRD serves as the foundation for TrustRail development. Feedback and refinements are encouraged to align with stakeholder needs.