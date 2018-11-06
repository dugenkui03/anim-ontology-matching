/*anim数据前置处理*/

-- delete from anim where length(term)>xx


/*取出anim和dbpedia中的term*/
-- update dbpedia set term = left(substring_index(content,'/',-1),length(substring_index(content,'/',-1))-1);


/*term中还有包含#和_的脏数据：dbpedia中的#使用sql去掉，anim中的下划线使用python程序调整—将下划线后的第一个字母用大写字母替换*/
-- select * from dbpedia where locate('#',term)!=0; -- 33条脏数据
-- select * from dbpedia where locate('_',term)!=0; -- 下划线不是分隔符

-- select * from anim where locate('_',term)!=0; -- 380

select term,left(substring_index(term,'#',-1),length(substring_index(term,'#',-1))-1) from dbpedia where locate('#',term)!=0;
 

