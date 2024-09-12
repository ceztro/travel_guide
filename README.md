Travel Guide Web Application

This repository contains the source code for the Travel Guide web application, a Flask-based app hosted on an Amazon EKS cluster. The infrastructure for the project is managed via Terraform, allowing for scalable and maintainable cloud resources.

Project Overview

The Travel Guide app is a web application hosted on AWS EKS with a PostgreSQL database managed by Amazon RDS. AWS Secrets Manager handles sensitive information such as database credentials, ensuring secure communication with AWS services.

The entire infrastructure and application deployment are managed across three repositories:

	1.	terraform_infrastructure: Provisions the AWS infrastructure (VPC, EKS, RDS, IAM, etc.).
	2.	ArgoCD_GitOps: Contains Kubernetes manifests and GitOps configuration for managing the application deployment and lifecycle using ArgoCD.
	3.	travel_guide: This repository, containing the Flask application and code to connect to the RDS database.

Key Technologies

	•	Flask: Python web framework for the web application.
	•	Amazon EKS: Managed Kubernetes service for running the application.
	•	Amazon RDS: Relational database service used to store application data.
	•	AWS Secrets Manager: Secure management of database credentials.
	•	ArgoCD: Continuous delivery tool to manage Kubernetes resources using GitOps.
	•	Terraform: Infrastructure-as-code for managing AWS cloud resources.
	•	GitHub Workflows: Continuous Integration pipelines for building, testing, and deploying the application automatically.


Features

	•	Dynamic Secrets Management: The app dynamically discovers the AWS-managed RDS secret and retrieves the credentials to securely connect to the database.
	•	RDS Integration: The app connects to an Amazon RDS database using the credentials fetched from AWS Secrets Manager.
	•	Modular Terraform Infrastructure: The infrastructure is broken into reusable Terraform modules for networking, Kubernetes, bastion hosts, RDS, and IAM roles.
	•	Kubernetes Deployment: The application is deployed on an EKS cluster and managed through ArgoCD, following GitOps principles.
