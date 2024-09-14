

# HardPick API

## Overview

The HardPick API is a Python Flask-based service designed to help users select the best PC specifications within a given budget. The API allows users to input their budget, and it returns optimal PC specs based on scraped prices, benchmarks, and a custom scoring function.

## Features

- **Budget Input**: Users can specify their maximum budget.
- **Specs Recommendation**: The API provides recommended PC specifications that offer the best performance for the given budget.
- **Price Scraping**: Retrieves current prices from various sources.
- **Benchmark Data**: Incorporates benchmarks to ensure high performance within the budget.

## Endpoints

### `GET /api`

**Description**: Retrieves recommended PC specs based on the provided budget.

**Parameters**:
- `budget` (float): The maximum budget for the PC build.
- `comp` (string): The Component for the PC build.

**Response**:
- `data` (string): Specs 
- `win` (object): Recommended PC specs 


