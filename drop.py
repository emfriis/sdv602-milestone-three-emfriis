from data.jsndrop.jsn_drop_service import jsnDrop
jsn_tok = "74c07043-ce1d-4a68-8c34-fd24639d439f"
jsnDrop = jsnDrop(jsn_tok,"https://newsimland.com/~todd/JSON")


jsnDrop.drop("tblUser")
jsnDrop.drop("tblChat")
