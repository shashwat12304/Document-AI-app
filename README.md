# 📄 Document AI Invoice Processing Script

This Python script processes invoice PDF files using Google Cloud Document AI and saves the outputs (processed PDF, entity data CSV, and low confidence score CSV) in corresponding folders within the input directory.

## 📘 Introduction to Document AI

Google Cloud Document AI uses machine learning to automatically classify, extract, and structure data from documents. It leverages state-of-the-art deep learning models to process documents like invoices, receipts, and contracts, enabling you to extract valuable information efficiently and accurately. For a detailed overview, refer to my [Document AI REST API article on Hashnode](https://shashwat12304.hashnode.dev/document-ai-rest-api-google-cloud).

## 🚀 Quickstart

### Installation

1. **Install the required Python packages**:
    ```bash
    pip install google-cloud-documentai pandas python-dotenv
    ```

2. **Enable Google Cloud Document AI API**: Ensure that you have Google Cloud credentials set up and the Document AI API enabled. You can find instructions [here](https://cloud.google.com/document-ai/docs/quickstart).

    - **Set Up Google Cloud Credentials**:
        1. Go to the Google Cloud Console.
        2. Create a new project or select an existing project.
        3. Enable the Document AI API for your project.
        4. Create a service account key:
            - Navigate to the "IAM & Admin" > "Service Accounts" page.
            - Click "Create Service Account".
            - Provide a name and description for the service account.
            - Assign the role "Document AI Editor".
            - Click "Create Key" and select "JSON" as the key type.
            - Save the generated JSON file to your computer.

3. **Set Up Environment Variables**: Create a `.env` file in the project directory and add your environment variables:
    ```ini
    GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
    INPUT_FOLDER=/path/to/input/folder
    PROCESSOR_ID=your_processor_id
    PROJECT_ID=your_project_id
    LOCATION=your_location
    ```

4. **Run the Script**: Execute the script with the specified input folder:
    ```bash
    python invoice_processing.py
    ```

## 🗂️ Input Folder Structure

The input folder should contain one or more invoice PDF files.

## 📂 Output Folder Structure

For each invoice PDF file in the input folder, the script creates a corresponding output folder with the same name as the PDF file (excluding the file extension). Inside each output folder, the following files are saved:

- **output.pdf**: Processed PDF file with entities highlighted.
- **output.csv**: CSV file containing entity data extracted from the PDF.
- **low_confidence_scores.csv**: CSV file containing entities with confidence scores below the specified threshold (default threshold is 50.0).

## 🔍 Example

Suppose you have an input folder named `invoices` containing the following invoice PDF files:
- `invoice1.pdf`
- `invoice2.pdf`

Run the script as follows:
```bash
python invoice_processing.py
```

The script will create output folders `invoice1` and `invoice2` within the `invoices` directory, and save the processed PDF, entity data CSV, and low confidence score CSV files in each output folder.

## 🔄 Workflow

1. **Initialization**: Load environment variables and set up Google Cloud credentials.
2. **Document Processing**: Process each PDF file using Google Cloud Document AI, extracting entity data and saving it to specified output files.
3. **Confidence Filtering**: Filter out entities with confidence scores below a specified threshold and save them to a separate CSV file.
4. **Output Generation**: Create structured output folders for each processed PDF file, containing the processed PDF, entity data CSV, and low confidence score CSV files.

## 🧩 Explanation of Classes and Functions

### `DocumentProcessor` Class

**Methods:**
- `__init__(self, project_id, location, processor_id, credentials_path)`: Initializes the DocumentProcessor with Google Cloud credentials.
- `process_invoice_pdf(self, pdf_path, output_dir)`: Processes a single PDF invoice and saves the results.
- `filter_low_confidence(self, df, output_folder, threshold=50.0)`: Filters entities with low confidence scores and saves them to a separate CSV file.

### `InvoiceFolderProcessor` Class

**Methods:**
- `__init__(self, input_folder, processor)`: Initializes the InvoiceFolderProcessor with the input folder and DocumentProcessor instance.
- `create_output_folder(self, processor_id)`: Creates an output folder for the processed invoices.
- `process_invoice_folder(self)`: Processes all PDF invoices in the specified input folder.

## ⚠️ Error Handling

| Error                         | Reason                                                  | Mitigation                                             |
|-------------------------------|---------------------------------------------------------|--------------------------------------------------------|
| FileNotFoundError             | Specified PDF file not found                            | Check the file path and ensure the file exists         |
| GoogleAPIError                | Issue with Google Cloud API                             | Verify API credentials and ensure API is enabled       |
| Environment Variable Missing  | Missing necessary environment variable                  | Ensure all required environment variables are set      |
| JSONDecodeError               | Error in parsing JSON credentials file                  | Check the JSON file for correctness                    |
| PermissionDeniedError         | Insufficient permissions for the service account        | Ensure the service account has appropriate permissions |
| OSError                       | Issues with file operations                             | Ensure correct file paths and permissions              |
| Unexpected Error              | Any other error                                         | Check the error message and debug accordingly          |

## 🌟 Contributing

If you find this project useful, please consider giving it a ⭐ star on GitHub! If you want to contribute, feel free to fork the repository, make changes, and submit a pull request.

- **Fork this repository**: Click on the 'Fork' button at the top right corner.
- **Create your feature branch**: 
    ```bash
    git checkout -b feature/your-feature-name
    ```
- **Commit your changes**:
    ```bash
    git commit -m 'Add some feature'
    ```
- **Push to the branch**:
    ```bash
    git push origin feature/your-feature-name
    ```
- **Create a new Pull Request**

---
## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.Feel free to suggest any improvements or open issues for bugs and enhancements. Thank you for your contributions!

---




