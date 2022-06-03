# Data Mesh

Great article from Martin Fowler: https://martinfowler.com/articles/data-monolith-to-mesh.html
- Unified warehouse problems: bottlenecked Data teams and pipelines are strongly coupled from raw to final

Good introduction video:  https://youtu.be/Wj7hTPcYIH8
- Think of a Data Mesh as a marketplace.
  - Data producers are sellers
    - Quality assurance responsibility falls to the seller
  - Data consumers are buyers
    - The buyer must be able to explore and select data without interaction with the seller
      - Thus data must be transparent and descriptive
  - The contract between producer and consumer must be stable
    - The underlying data may evolve without interaction between teams
- How to do this:
  - Create standardized templates for data infrastructure
  - Governance must be standardized: single interface to deal with all data
    - including monitoring, auditing, access control, infrastructure



Like:
- 
























