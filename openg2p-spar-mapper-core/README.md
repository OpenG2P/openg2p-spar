# OpenG2P SPAR Mapper Core

[![Pre-commit Status](https://github.com/OpenG2P/openg2p-spar-mapper-api/actions/workflows/pre-commit.yml/badge.svg?branch=develop)](https://github.com/OpenG2P/openg2p-spar-mapper-api/actions/workflows/pre-commit.yml?query=branch%3Adevelop)
[![Build Status](https://github.com/OpenG2P/openg2p-spar-mapper-api/actions/workflows/test.yml/badge.svg?branch=develop)](https://github.com/OpenG2P/openg2p-spar-mapper-api/actions/workflows/test.yml?query=branch%3Adevelop)
[![codecov](https://codecov.io/gh/OpenG2P/openg2p-spar-mapper-api/branch/develop/graph/badge.svg)](https://codecov.io/gh/OpenG2P/openg2p-spar-mapper-api)
[![openapi](https://img.shields.io/badge/open--API-swagger-brightgreen)](https://validator.swagger.io/?url=https://raw.githubusercontent.com/OpenG2P/openg2p-spar-mapper-api/develop/api-docs/generated/openapi.json)
[![PyPI](https://img.shields.io/pypi/v/openg2p-spar-mapper-api?label=pypi%20package)](https://pypi.org/project/openg2p-spar-mapper-api)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/openg2p-spar-mapper-api)](https://pypi.org/project/openg2p-spar-mapper-api)

**FastAPI-based core library providing Beneficiary ID and Financial Account Mapping Services**

A comprehensive microservice library implementing G2P Connect API standards for linking, resolving, updating, and unlinking beneficiary identities with their financial accounts.

## 🎯 Key Features

- **Link**: Create mappings between Beneficiary IDs and Financial Accounts
- **Resolve**: Query and retrieve FA information for given IDs
- **Update**: Modify existing ID-FA mappings
- **Unlink**: Remove mappings between IDs and FAs
- **DFSP Management**: Manage Digital Financial Service Providers (Banks, Wallets, etc.)
- **Strategy-based Construction**: Regex-based ID/FA construction and deconstruction
- **Async/Await**: Full async support for high-performance operations
- **G2P Connect Compliant**: Implements official G2P Connect API standards

## 📚 Documentation

Comprehensive documentation is available:

| Document | Purpose | Audience |
|----------|---------|----------|
| [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) | Core concepts and architecture | All developers |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | API reference and examples | API consumers |
| [EXTENSION_GUIDE.md](EXTENSION_GUIDE.md) | Customization and extension | Backend developers |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Deployment and operations | DevOps/Operations |
| [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) | Navigation and learning paths | All users |

**👉 [Start with DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for guided learning paths!**

## 🚀 Quick Start

### Installation

```bash
pip install openg2p-spar-mapper-core
```

### Basic Usage

```python
from openg2p_spar_mapper_core.services import MapperService
from openg2p_spar_models.schemas import LinkRequest

# Initialize service
mapper_service = MapperService()

# Create a link
link_request = LinkRequest(...)
response = await mapper_service.link(link_request)
```

### Running the API

```bash
# Development
uvicorn openg2p_spar_bene_portal_api.app:app --reload

# Production
gunicorn openg2p_spar_bene_portal_api.app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

## 📋 Requirements

- Python 3.9+
- PostgreSQL 12+
- FastAPI 0.100+
- SQLAlchemy 2.0+
- Pydantic 2.0+

## 🏗️ Architecture

```
openg2p-spar-mapper-core/
├── services/              # Core business logic
│   ├── mapper.py          # Link, Resolve, Update, Unlink
│   ├── request_validations.py
│   ├── id_fa_mapping_validations.py
│   ├── response_helper.py
│   └── dfsp_service.py    # DFSP provider management
├── helpers/               # Utility functions
│   └── strategy_helper.py # ID/FA construction
├── exceptions/            # Custom exceptions
└── tests/                 # Unit and integration tests
```

## 🔌 API Endpoints

### Mapper Operations
- `POST /link` - Create ID-FA mappings
- `POST /resolve` - Query FA information
- `POST /update` - Modify mappings
- `POST /unlink` - Remove mappings

### DFSP Management
- `GET /dfsp/providers` - Get all provider types
- `GET /dfsp/providers/{type}` - Get specific provider type
- `GET /dfsp/providers/{type}/values` - Get provider values
- `GET /dfsp/values/{code}` - Get provider by code
- `GET /dfsp/values/{parent_id}/children` - Get hierarchical children

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=openg2p_spar_mapper_core tests/

# Run specific test
pytest tests/test_async_mapper_controller.py
```

## 📖 Example: Link API

```bash
curl -X POST http://localhost:8004/link \
  -H "Content-Type: application/json" \
  -d '{
    "request_header": {
      "version": "1.0.0",
      "message": "Link Request",
      "action": "link",
      "correlation_id": "uuid",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    "request_body": {
      "request_payload": {
        "link_request": [
          {
            "reference_id": "ref123",
            "id": "ID123",
            "fa": "FA456",
            "name": "John Doe",
            "phone_number": "+1234567890"
          }
        ]
      }
    }
  }'
```

## 🔐 Security

- Input validation on all requests
- SQL injection prevention via SQLAlchemy ORM
- CORS support for cross-origin requests
- Environment-based configuration
- Secure password handling

## 📊 Performance

- Async/await for non-blocking operations
- Connection pooling for database
- Caching support for frequently accessed data
- Batch processing capabilities
- Query optimization with indexes

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This repository is licensed under [MPL-2.0](LICENSE).

## 🔗 Resources

- [OpenG2P Documentation](https://docs.openg2p.org/)
- [G2P Connect Standards](https://g2p-connect.org/)
- [GitHub Repository](https://github.com/OpenG2P/openg2p-spar-mapper-api)
- [PyPI Package](https://pypi.org/project/openg2p-spar-mapper-core/)

## 💬 Support

- 📖 [Documentation](DOCUMENTATION_INDEX.md)
- 🐛 [GitHub Issues](https://github.com/OpenG2P/openg2p-spar-mapper-api/issues)
- 💬 [Community Forum](https://community.openg2p.org/)

---

**Made with ❤️ by the OpenG2P Team**
