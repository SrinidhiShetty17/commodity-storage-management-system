# Commodity Storage Management System

## Overview
A backend-driven system designed to manage and analyze commodity storage across multiple factories. The system tracks inventory levels, logs commodity transactions, and enables data-driven insights to optimize stock management and reduce operational inefficiencies.

## Problem Statement
Factories often rely on manual or fragmented systems to manage commodity storage, leading to overstocking, understocking, and lack of visibility into consumption trends. This project aims to centralize inventory data and provide analytical insights for better decision-making.

## Tech Stack
- MySQL (Relational Database)
- SQL
- Python (planned for backend & analysis)

## Core Features
- Factory-wise commodity management
- Centralized inventory storage tracking
- Transaction logging (IN / OUT)
- Historical data for consumption analysis

## Database Design
The database consists of the following tables:
- `factories` – stores factory details
- `commodities` – stores commodity information
- `storage` – maintains current stock levels
- `transactions` – logs historical inventory movement

## Project Structure
