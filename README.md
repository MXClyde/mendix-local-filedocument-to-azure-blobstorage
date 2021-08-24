# mendix-local-filedocument-to-azure-blobstorage

- Script to upload Mendix FileDocuments from local storage to Azure Blob Storage
- Modification of the Local Storage > AWS S3 migration script by Jouke Waleson (https://gist.github.com/jtwaleson/5c00642165655febfaaf4c6b2867055a)
===
Context:

Older Mendix versions (<7) used a different naming syntax for storing FileDocuments on disk. Above Python scripts enable the conversion from this older format to the new format for subsequent upload to S3 or Azure Blob Storage.
