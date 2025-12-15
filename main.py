import json
import csv
import datetime
from database import conectar, criar_tabelas, inserir_templates

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

SEPARADOR = "-" * 50

def cabecalho():
    print(SEPARADOR)
    print("📄 SISTEMA DE AUTOMATIZAÇÃO DE RELATÓRIOS")
    print(" Versão 1.0")
    print(SEPARADOR)


def listar_templates():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM templates_relatorios")
    templates = cursor.fetchall()
    conn.close()
    return templates

def obter_template(template_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT template FROM templates_relatorios WHERE id = ?",
        (template_id,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


def extrair_campos(template):
    campos = []
    partes = template.split("{")
    for parte in partes[1:]:
        campo = parte.split("}")[0]
        if campo not in campos and campo != "data":
            campos.append(campo)
    return campos


def preencher_template(template):
    print("\n📝 Preenchimento do Relatório")
    print(SEPARADOR)

    campos = extrair_campos(template)
    dados = {}

    dados["data"] = datetime.date.today().strftime("%d/%m/%Y")

    for campo in campos:
        valor = input(f"➡️  {campo.capitalize()}: ")
        dados[campo] = valor

    relatorio = template.format(**dados)
    return relatorio, dados


def gerar_txt(conteudo):
    with open("relatorio.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)

def gerar_json(dados):
    with open("relatorio.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def gerar_csv(dados):
    with open("relatorio.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(dados.keys())
        writer.writerow(dados.values())


def gerar_pdf(conteudo):
    arquivo_pdf = "relatorio.pdf"
    c = canvas.Canvas(arquivo_pdf, pagesize=A4)

    largura, altura = A4
    x = 2 * cm
    y = altura - 2 * cm

    c.setFont("Helvetica", 11)

    for linha in conteudo.split("\n"):
        if y < 2 * cm:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = altura - 2 * cm

        c.drawString(x, y, linha)
        y -= 14

    c.save()


def menu():
    cabecalho()

    templates = listar_templates()
    if not templates:
        print("⚠️ Nenhum template disponível.")
        return

    print("\n📂 Templates disponíveis:\n")
    for t in templates:
        print(f" [{t[0]}] {t[1]}")

    print(SEPARADOR)

    try:
        escolha = int(input("👉 Escolha o número do template: "))
    except ValueError:
        print("\n❌ Entrada inválida.")
        return

    template = obter_template(escolha)
    if not template:
        print("\n❌ Template não encontrado.")
        return

    relatorio, dados = preencher_template(template)

    gerar_txt(relatorio)
    gerar_json(dados)
    gerar_csv(dados)
    gerar_pdf(relatorio)

    print("\n" + SEPARADOR)
    print("✅ Relatórios gerados com sucesso!")
    print("📁 Arquivos criados:")
    print(" - relatorio.txt")
    print(" - relatorio.json")
    print(" - relatorio.csv")
    print(" - relatorio.pdf")
    print(SEPARADOR)


if __name__ == "__main__":
    criar_tabelas()
    inserir_templates()
    menu()