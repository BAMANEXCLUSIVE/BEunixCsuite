import os

def generate_uml(output_file):
    uml_code = """
    @startuml
    ' Define parent class
    class ParentClass {
        + String parentAttribute
        + void parentMethod()
    }
    
    ' Define child class
    class ChildClass {
        + String childAttribute
        + void childMethod()
    }
    
    ' Relationship
    ParentClass <|-- ChildClass

    ' Add hyperlinks
    ParentClass : [[https://github.com/BAMANEXCLUSIVE/skills-introduction-to-github/issues/1#issue-2891216224]]
    ChildClass : [[https://github.com/BAMANEXCLUSIVE/skills-introduction-to-github/issues/1#issue-2891216224]]

    note right of ParentClass
      This is the ParentClass. For more details, visit
      [[https://github.com/BAMANEXCLUSIVE/skills-introduction-to-github/issues/1#issue-2891216224]].
    end note

    note right of ChildClass
      This is the ChildClass. For more details, visit
      [[https://github.com/BAMANEXCLUSIVE/skills-introduction-to-github/issues/1#issue-2891216224]].
    end note
    @enduml
    """
    
    with open(output_file, 'w') as file:
        file.write(uml_code)

if __name__ == "__main__":
    output_file = "diagram.puml"
    generate_uml(output_file)
    print(f"PlantUML code written to {output_file}")