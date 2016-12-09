# Architecture

Overview:  

![Architecture Diagram](images/architecture.jpg)

Apache/Flask 
- Justifications:
- Limiations:

MySQL 
- Justifications: 
- Limitations:

Python Injestion Scripts
- Justifications:
- Limitations:

S3 Datalake
- Justifications: In its current incarnation our datalake is basically a backup store in case the datasources ever disapear all together. The main requirment is that the data be resilient and accessible in the future. It will rarely, if ever be accessed, so speed of access is not a major factor of consideration.
- Limitations: Not the fastest datalake implementation, but speed is not essention for our proposed use.

[Return to Documentation Index](index.md)
