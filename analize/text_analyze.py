import os

kb_path="E:\\animworkspace\\3dsma\\"

def tra_dir(path):
	if os.path.isdir(path):
		paths=os.listdir(path)
		for p in paths:
			abs_p=os.path.join(path,p)
			tra_dir(abs_p)
	if ".java"  in str(path):
			text_finder(path,"F:")

def text_finder(file_path,xxx_str):
	try:
		with open(file_path,encoding="utf-8") as owl_file:
			owl_content=owl_file.readlines()
			for line in owl_content :
				if xxx_str in line :
					print(file_path+"dugenkui"+line)
					break
	except:
		try:
			# print("start with gbk"+str(file_path))
			with open(file_path) as owl_file:
				owl_content = owl_file.readlines()
				for line in owl_content:
					if xxx_str in line:
						print(file_path + ":" + line)
						break
		except:
			# print("抛弃：" + str(file_path))
			pass


tra_dir(kb_path)


"""
C:\ontologyOWL\AllOwlFile\LHH_Wind\Effect.owl:  xml:base="http://www.owl-ontologies.com/OntologyEffect.owl">

C:\ontologyOWL\AllOwlFile\zhaoOWL\ColorAndLight.owl:    xmlns="http://www.owl-ontologies.com/Ontology1291624979.owl#"
C:\ontologyOWL\AllOwlFile\HLLight\TheNewLight.owl:    xmlns="http://www.owl-ontologies.com/Ontology1457533409.owl#"
C:\ontologyOWL\AllOwlFile\JialiOWL\ActionPart.owl:  xml:base="http://www.owl-ontologies.com/OntologyActionFogExpression.owl">
C:\ontologyOWL\AllOwlFile\FireworkOWL\FireworkOWL.owl:    xmlns="http://www.owl-ontologies.com/Ontology1488534407.owl#"
C:\ontologyOWL\AllOwlFile\LHH_Wind\Effect.owl:  xml:base="http://www.owl-ontologies.com/OntologyEffect.owl">
C:\ontologyOWL\AllOwlFile\InterAction\Interaction.owl:    xmlns="http://www.owl-ontologies.com/Ontology1496659417.owl#"
C:\ontologyOWL\AllOwlFile\MakeBoats\MakeBoats.owl:    xmlns="http://www.owl-ontologies.com/Ontology1491747683.owl#"
C:\ontologyOWL\AllOwlFile\zhenOWL\zhen.owl:  xml:base="http://www.owl-ontologies.com/Ontologyzhen.owl">
C:\ontologyOWL\AllOwlFile\Layout\sumo_phone3.owl:    xmlns="http://www.owl-ontologies.com/Ontology1357699817.owl#"
C:\ontologyOWL\AllOwlFile\Event\Event.owl:    xmlns="http://www.owl-ontologies.com/Ontology1448934359.owl#"


"""