import pandas as pd
from Tools.scripts.dutree import display
from IPython.display import display

tabela_vendas = pd.read_excel("D:/Disco D/Intensivão Python/Vendas.xlsx")
# display(tabela_vendas)

tabela_faturamento = tabela_vendas[["ID Loja", "Valor Final"]].groupby("ID Loja").sum()
tabela_faturamento = tabela_faturamento.sort_values(by="Valor Final", ascending=False)
# display(tabela_faturamento)

tabela_quantidade = tabela_vendas[["ID Loja", "Quantidade"]].groupby("ID Loja").sum()
# display(tabela_quantidade)

ticket_medio = (tabela_faturamento["Valor Final"] / tabela_quantidade["Quantidade"]).to_frame()
ticket_medio = ticket_medio.rename(columns={0: "Ticket Medio"})
# display(ticket_medio)


def enviar_email(nome_da_loja, tabela):
    import smtplib
    import email.message

    server = smtplib.SMTP('smtp.gmail.com:587')
    corpo_email = f"""
  <p>Prezados,</p>
  <p>Segue relatório de vendas</p>
  {tabela.to_html()}
  <p>Qualquer dúvida estou a disposição</p>
  """  # vm editar

    msg = email.message.Message()
    msg['Subject'] = f"Relatório de Vendas - {nome_da_loja}"  # vm editar

    msg['From'] = 'brunagirlpaula2002@gmail.com'  # vm editar
    msg['To'] = 'paulohm2309@gmail.com'  # vm editar
    password = "senha"  # vm editar
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')


tabela_completa = tabela_faturamento.join(tabela_quantidade).join(ticket_medio)
enviar_email("Diretoria", tabela_completa)

lista_lojas = tabela_vendas["ID Loja"].unique()

for loja in lista_lojas:
    tabela_loja = tabela_vendas.loc[tabela_vendas["ID Loja"] == loja, ["ID Loja", "Quantidade", "Valor Final"]]
    tabela_loja = tabela_loja.groupby("ID Loja").sum()
    tabela_loja["Ticket Medio"] = tabela_loja["Valor Final"] / tabela_loja["Quantidade"]
    enviar_email(loja, tabela_loja)

