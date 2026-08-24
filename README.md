# Sponsor Connect

> A Django web application for connecting event organizers and colleges with potential sponsors through event listings, sponsorship requests and funding-history workflows.

**Python · Django · MySQL · HTML/CSS**

## Overview

Sponsor Connect models both sides of the sponsorship process:

- **Sponsors** can maintain profiles and sponsorship opportunities.
- **Colleges / organizers** can publish events and funding requirements.
- Both sides can create and track sponsorship requests.
- Accepted sponsorship activity can be represented through sponsorship-history records.

This is an earlier full-stack project and is kept as part of the repository history; newer projects on this profile better represent my current engineering practices.

## Data model

The Django application includes domain models for:

- sponsors
- colleges
- sponsor events
- college events
- sponsorship requests
- request status (`pending`, `accepted`, `rejected`)
- sponsor history
- college sponsorship history

A sponsorship request connects a sponsor, college and event while recording the proposed price, deliverables and current request state.

## Repository structure

```text
sponsor-connect/
├── manage.py
├── sponsorship_site/      # Django project configuration
└── listings/              # Main application
    ├── models.py          # Sponsorship domain models
    ├── views.py           # Application views and workflows
    ├── forms.py           # Django forms
    ├── serializers.py     # Serialization layer
    ├── urls.py            # Application routes
    ├── middleware.py
    ├── templates/         # Server-rendered UI
    └── static/            # Static assets
```

## Local setup

### Prerequisites

- Python 3
- Django
- MySQL
- `mysqlclient`

Clone the repository:

```bash
git clone https://github.com/Krishh003/sponsor-connect.git
cd sponsor-connect
```

Configure the database for your local MySQL instance, then initialize Django:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The development server will be available at `http://127.0.0.1:8000/` by default.

## Notes

This repository predates the more production-oriented backend and ML systems featured on my profile. It is retained to show the progression from a conventional Django/MySQL application toward the service, retrieval and ML architectures used in my newer work.
