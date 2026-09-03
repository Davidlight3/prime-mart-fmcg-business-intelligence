# ==========================================
# PrimeMart FMCG Analytics Platform
# Configuration File
# ==========================================

from pathlib import Path

# Base Project Folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Folders
RAW_DATA = BASE_DIR / "01_Raw_Data"
GENERATED_DATA = BASE_DIR / "02_Generated_Data"

# Create folders automatically if they don't exist
RAW_DATA.mkdir(exist_ok=True)
GENERATED_DATA.mkdir(exist_ok=True)

# Random Seed
RANDOM_SEED = 42

# Dataset Sizes
NUM_PRODUCTS = 5000
NUM_CUSTOMERS = 50000
NUM_SUPPLIERS = 300
NUM_STORES = 80
NUM_EMPLOYEES = 800
NUM_PROMOTIONS = 2000
NUM_SALES = 500000
NUM_PURCHASES = 150000
NUM_RETURNS = 20000

# Project Information
PROJECT_NAME = "PrimeMart FMCG Analytics Platform"
PROJECT_VERSION = "1.0.0"

# Currency
CURRENCY = "NGN"

# Default Country
COUNTRY = "Nigeria"

# ==========================================================
# DATE DIMENSION
# ==========================================================

DATE_START = "2015-01-01"

DATE_END = "2030-12-31"