import os
from google.cloud import documentai_v1 as documentai
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
class DocumentProcessor:
    def __init__(self, project_id, location, processor_id, credentials_path):
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            self.location = location
            self.project_id = project_id
            self.processor_id = processor_id
            self.client_options = {"api_endpoint": f"{self.location}-documentai.googleapis.com"}
            self.client = documentai.DocumentProcessorServiceClient(client_options=self.client_options)
            self.name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"
        except Exception as e:
            print(f"Error initializing DocumentProcessor: {e}")

    def process_invoice_pdf(self, pdf_path, output_dir):
        """
        Process a PDF invoice using Google Document AI and save the results.

        Args:
            pdf_path (str): The path to the PDF file.
            output_dir (str): The directory to save the processed output.
        """
        try:
            with open(pdf_path, "rb") as image:
                image_content = image.read()
            document = {"content": image_content, "mime_type": "application/pdf"}
            request = {"name": self.name, "raw_document": document}

            result = self.client.process_document(request=request)
            doc = result.document
            pdf_filename = os.path.basename(pdf_path)
            output_folder = os.path.join(output_dir, f"{os.path.splitext(pdf_filename)[0]}_{self.processor_id}")
            os.makedirs(output_folder, exist_ok=True)
            output_pdf_path = os.path.join(output_folder, "output.pdf")
            with open(output_pdf_path, "wb") as f:
                f.write(doc.content)
            entities = doc.entities
            types = [entity.type_ for entity in entities]
            values = [entity.mention_text for entity in entities]
            confidence = [round(entity.confidence * 100, 2) for entity in entities]
            df = pd.DataFrame({'Type': types, 'Value': values, 'Confidence': confidence})
            output_csv_path = os.path.join(output_folder, "output.csv")
            df.to_csv(output_csv_path, index=False)
            self.filter_low_confidence(df, output_folder)
        except FileNotFoundError:
            print(f"Error: File not found - {pdf_path}")
        except documentai.exceptions.GoogleAPIError as e:
            print(f"Google API Error: {e}")
        except Exception as e:
            print(f"Unexpected error processing {pdf_path}: {e}")

    def filter_low_confidence(self, df, output_folder, threshold=50.0):
        """
        Filter entities with low confidence scores and save them to a separate CSV file.

        Args:
            df (pd.DataFrame): The DataFrame containing entity data.
            output_folder (str): The directory to save the filtered results.
            threshold (float): The confidence threshold below which entities are filtered.
        """
        try:
            low_conf_df = df[df['Confidence'] < threshold]
            low_conf_csv_path = os.path.join(output_folder, "low_confidence_scores.csv")
            low_conf_df.to_csv(low_conf_csv_path, index=False)
        except Exception as e:
            print(f"Error filtering low confidence scores: {e}")

class InvoiceFolderProcessor:
    def __init__(self, input_folder, processor):
        self.input_folder = input_folder
        self.processor = processor

    def create_output_folder(self, processor_id):
        """
        Create an output folder for the processed invoices.

        Args:
            processor_id (str): The processor ID used for naming the folder.

        Returns:
            str: The path to the created output folder.
        """
        try:
            output_folder = os.path.join(self.input_folder, f"{os.path.basename(self.input_folder)}_{processor_id}")
            os.makedirs(output_folder, exist_ok=True)
            return output_folder
        except Exception as e:
            print(f"Error creating output folder: {e}")

    def process_invoice_folder(self):
        """
        Process all PDF invoices in the specified input folder.
        """
        try:
            processor_folder = self.create_output_folder(self.processor.processor_id)
            for root, _, files in os.walk(self.input_folder):
                if root != processor_folder and not any(self.input_folder in sub for sub in root.split(os.path.sep)):
                    subfolder_name = os.path.relpath(root, self.input_folder)
                    if not any(parent in subfolder_name for parent in self.input_folder.split(os.path.sep)):
                        subfolder_output = os.path.join(processor_folder, subfolder_name)
                        os.makedirs(subfolder_output, exist_ok=True)
                        for filename in files:
                            if filename.endswith(".pdf"):
                                pdf_path = os.path.join(root, filename)
                                self.processor.process_invoice_pdf(pdf_path, subfolder_output)
        except Exception as e:
            print(f"Error processing invoice folder: {e}")

if __name__ == "__main__":
    try:
        input_folder = os.getenv("INPUT_FOLDER")
        processor_id = os.getenv("PROCESSOR_ID")
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.getenv("PROJECT_ID")
        location = os.getenv("LOCATION")

        if not all([input_folder, processor_id, credentials_path, project_id, location]):
            raise ValueError("Some environment variables are missing.")

        processor = DocumentProcessor(project_id, location, processor_id, credentials_path)
        invoice_processor = InvoiceFolderProcessor(input_folder, processor)
        invoice_processor.process_invoice_folder()
    except Exception as e:
        print(f"Error in main execution: {e}")
