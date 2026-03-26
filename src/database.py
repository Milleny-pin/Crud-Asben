import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def cadastrar_com_foto(self, nome, cpf, data_nasc, caminho_foto_local):
        try:
            foto_url = None
            
            if caminho_foto_local:
                nome_arquivo_remoto = f"{cpf}.jpg"
                
                with open(caminho_foto_local, 'rb') as f:
                    self.supabase.storage.from_("fotos_perfil").upload(
                        path=nome_arquivo_remoto,
                        file=f,
                        file_options={"content-type": "image/jpeg", "upsert": "true"}
                    )
                
                res_url = self.supabase.storage.from_("fotos_perfil").get_public_url(nome_arquivo_remoto)
                foto_url = res_url
            
            dados_usuario = {
                "nome": nome,
                "cpf": cpf,
                "data_nascimento": data_nasc,
                "foto_url": foto_url  
            }
            
            self.supabase.table("Pessoa").insert(dados_usuario).execute()
            return True, "Cadastro e Foto salvos com sucesso!"

        except Exception as e:
            return False, f"Erro ao cadastrar: {str(e)}"

    def listar_usuarios(self):
        try:
            res = self.supabase.table("Pessoa").select("*").execute()
            return res.data
        except Exception as e: 
            print(f"Erro ao buscar: {e}")
            return []