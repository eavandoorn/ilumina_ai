from crewai import Agent

# The Architect: Focuses on high-level structure and requirements
architect = Agent(
    role='System Architect',
    goal='Design a scalable database schema and API structure for an e-commerce platform.',
    backstory="""You are an expert software architect with 10 years of experience in 
    distributed systems. You specialize in Django and PostgreSQL. Your goal is to 
    ensure that the system is modular, secure, and follows DRY principles.""",
    allow_delegation=False,
    verbose=True
)

# The Developer: Focuses on writing clean, tested code
developer = Agent(
    role='Full-Stack Developer',
    goal='Implement features based on the architect\'s specifications using Django and Tailwind.',
    backstory="""You are a senior developer who writes clean, production-ready Python. 
    You excel at creating reusable components and integrating third-party APIs like Stripe.""",
    allow_delegation=False,
    verbose=True
)