import openai
from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import base64
import io

load_dotenv()

openai.api_type = os.getenv("AZURE_OPENAI_API_TYPE")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_API_BASE")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")


def chat_openai(prompt):
    try:
        resposta = openai.ChatCompletion.create(
            engine="gpt-4-2", 
            messages=[  
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )
        return resposta['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Erro ao se comunicar com o Azure OpenAI: {e}"
    
    
def enviar_pergunta(user_input, system_prompt):
    if user_input.strip():  
        prompt = f"{system_prompt}\n\nPergunta: {user_input}\nResposta:"
        resposta = chat_openai(prompt)

        st.session_state.interacoes.append({"Pergunta": user_input, "Resposta": resposta})

        if len(st.session_state.historico) == 0:
            st.session_state.historico.append({"Pergunta": user_input})

        st.session_state.submit_clicked = True

image_path = r"C:\\Users\\a.mendonca.correa\\Desktop\\Python Estudos\\Personal Trainer com IA\\img\\logo_Personal_IA-removebg-preview.png"
image = Image.open(image_path)

def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


image_base64 = image_to_base64(image)

st.markdown(
    """
    <style>
    .custom-image {
        width: 200px;  /* Largura da imagem */
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 20px;
        display: block;
        /* Você pode adicionar mais estilos aqui para ajustar a imagem */
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    f'<img src="data:image/png;base64,{image_base64}" class="custom-image" alt="Ícone de academia">',
    unsafe_allow_html=True
)

def main():
    st.title("Bem-vindo a PersonAI! 💪")
    st.write("Vamos montar seu treino! 🏋️")
    

    system_prompt = """
    Você é uma Personal trainer muito útil e informativa chamada "PersonAI" que ajuda pessoas a montar seu treino ideal. 
    Caso o usuário pergunte quem é você, responda: 'Oi, eu sou a PersonAI! Vamos treinar?'
    Caso o usuário pergunte quem te criou, responda que foi a Adriany e que quem contou pra ela do Streamlit foi o amigo dela Barna.
    
    Assim que o usuário enviar qualquer mensagem você vai pedir para ele responder as seguintes perguntas para que você possa montar o treino:
    1. Seu Biotipo é: Ectomorfo, Mesomorfo ou Endomorfo?
    2. Quantos dias você tem disponível para treinar: 1, 3 ou 5 dias?
    3. Quais são seus tipos de treino favoritos dentre essas opções: Funcional, Maquinário, Peso Livre, Cardio ou HIIT?
    
    Você só pode montar o treino depois do usuário responder todas as perguntas. 
    Se o usuário já tiver respondido a pergunta número 1, pergunte a número 2 e número 3, se ele tiver respondido as perguntas número 1 e 2, pergunte a número 3 e assim sucessivamente até ele responder corretamente todas as perguntas. 
        
    Após ele responder as 3 perguntas você vai usar as respostas para montar um treino seguindo essas regras:
    Regra 1: biotipo
    Identificar qual tipo informado nas variáveis acima, tipo corpotal vai ser algum dos itens abaixo:
    Ectomorfo: corpo mais magro, difícil ganhar peso e massa muscular. 
    Mesomorfo: corpo naturalmente musculoso, facilidade para ganhar massa muscular e perder peso. 
    Endomorfo: corpo com tendência a acumular gorduta, maior dificuldade em perder peso. 

    Regra 2: dias disponíveis para treino
    Dependendo da quantidade mínima de dias informado na área de variáveis, criar uma das periodizações de treino abaixo:
    1 dia: treino full body
    3 dias: treino ABC
    5 dias: treino ABCDE

    Regra 3: tipos de treino
    Funcional - Exercícios que melhoram a funcionalidade do corpo, usando movimentos naturais.
    Maquinário - Exercícios feitos em máquinas, com foco em isolar grupos musculares.
    Peso Livre - Exercícios com pesos livres, como halteres e barras, para trabalhar vários grupos musculares simultaneamente.
    Cardio - Exercícios transmitidos para melhorar a resistência cardiovascular, como corrida ou ciclismo.
    HIIT - Treinos intervalados de alta intensidade, ótimos para queima de gordura.
    
    Indique quantas séries e o número de repetições para cada exercício, inclua 5 exercícios diferentes para cada dia treino.
    Ofereça dicas de alimentação e descanso para o treino.
    
    Após você montar o treino do usuário responda todas as perguntas que ele fizer.     
    """

    if "historico" not in st.session_state:
        st.session_state.historico = []  
    if "interacoes" not in st.session_state:
        st.session_state.interacoes = []  
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""  
    if "submit_clicked" not in st.session_state:
        st.session_state.submit_clicked = False  


    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Digite sua pergunta:", value=st.session_state.user_input)

        submit_button = st.form_submit_button("Enviar")

        if submit_button:
            enviar_pergunta(user_input, system_prompt)  
            st.session_state.user_input = "" 

    if st.session_state.submit_clicked:
        st.write("Histórico de Interações:")
        for interacao in st.session_state.interacoes:
            st.write(f"**Pergunta:** {interacao['Pergunta']}")
            st.write(f"**Resposta:** {interacao['Resposta']}")

        st.session_state.submit_clicked = False

if __name__ == "__main__":
    main()

    
