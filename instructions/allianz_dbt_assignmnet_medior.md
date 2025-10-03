**Assignment Overview**

Objective:
Build a data transformation pipeline using dbt to implement a Data Vault model on a chosen database. The assignment will assess the candidate's ability to use dbt core/cloud features effectively, including model creation, testing, documentation, and logging.Database:
Candidates can choose from PostgreSQL, Snowflake, or BigQuery.

**Assignment Details**

**1. Data Vault Model Implementation**

Task:

* Design and implement a simple Data Vault model using dbt. The model should include:
  + Hubs: Create at least two hubs (e.g., Customer Hub, Product Hub).
  + Links: Create at least one link table to connect the hubs (e.g., Customer-Product Link).
  + Satellites: Create satellite tables for each hub to store descriptive attributes.

Instructions:

* Use dbt to define and build the models.
* Ensure that the models are modular and follow best practices for Data Vault modeling.

**2. Data Transformation**

Task:

* Load sample data into the raw layer of the database.
* Use dbt to transform the raw data into the Data Vault model.

Instructions:

* Write SQL transformations in dbt models to populate the hubs, links, and satellites.
* Ensure transformations are efficient and maintainable.

**3. Testing**

Task:

* Implement dbt tests to ensure data quality and model integrity.

Instructions:

* Use dbt's built-in tests (e.g., unique, not\_null) and create custom tests as needed.
* Document the purpose and results of each test.

**4. Documentation**

Task:

* Document the dbt project, including model descriptions and data lineage.

Instructions:

* Use dbt's documentation features to provide clear and concise documentation.
* Include a README file explaining the project structure and how to run the models.

**5. Logging and Debugging**

Task:

* Run the dbt pipeline and capture logs.

Instructions:

* Use dbt's logging features to track the execution of models.
* Share logs that demonstrate successful execution and any debugging steps taken.

**Deliverables**

1. dbt Project Files:
   * All dbt model files, tests, and documentation.
2. Test Results:
   * A summary of test results, including any issues encountered and how they were resolved.
3. Execution Logs:
   * Logs from running the dbt pipeline, highlighting key steps and any errors encountered.
4. Documentation:
   * A README file with instructions on how to set up and run the dbt project.

**Evaluation Criteria**

* Correctness: Accuracy of the Data Vault model and transformations.
* Testing: Coverage and effectiveness of tests.
* Documentation: Clarity and completeness of project documentation.
* Debugging: Ability to identify and resolve issues using logs.
* Explain Architectural Concepts: Provide simplified explanations of architectural concepts for similar projects.
* Define Pathway for Junior/Medior Developers: Outline a clear development pathway for junior and mid-level developers.
* Set Up Architecture for the Team: Assist in setting up the architecture for the team, including best coding practices and optimal hierarchy.
* Set Up YAML Files: Guide us on how to properly set up YAML files.