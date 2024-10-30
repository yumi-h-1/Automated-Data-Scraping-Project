# Automated Data Scraping Project

## Objectives
- Build a consistent database of regulatory and Health Technology Assessment (HTA) guidance on medicines for analysis and statistics.
- Focus on stepwise data collection and automation from European Medicines Agency (EMA) and National Institute for Health and Care Excellence (NICE) sources.

## AI Utilization
- **Model**: GPT-4o mini by OpenAI was chosen for its efficiency and cost-effectiveness within the 3-month timeline, rather than using Llama 3.1.
- **Functionality**: Extracts structured data from unstructured PDFs (e.g., EMA procedure steps) and web pages (e.g., EMA and NICE websites).
- **Outcome**: Data is saved to a structured Excel or CSV file for ongoing analysis.

## Project Progress
### EMA Data Scraping
- **Script Completion**: Initial framework for scraping EMA data is ready; collects data and exports it to an Excel file.
- **Improvements Needed**: Enhance model precision for accurately interpreting unstructured text.
- **Output**: Excel file named `final_EMA_dataset`, capturing details like medicine name, brand, and therapy area.
