-- 从URI中提取term：没有分隔符和大小写

select content,left(substring_index(content,'ontology/',-1),length(substring_index(content,'ontology/',-1))-1) from dbpedia ;
update update dbpedia set term = left(substring_index(content,'/',-1),length(substring_index(content,'/',-1))-1);

select content,left(substring_index(content,'.owl#',-1),length(substring_index(content,'.owl#',-1))-1) from anim;
update anim set term = left(substring_index(content,'.#',-1),length(substring_index(content,'.#',-1))-1);