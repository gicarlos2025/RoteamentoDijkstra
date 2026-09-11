import os
import random
import networkx as nx
import pandas as pd
from flask import Flask, jsonify, render_template, request, send_from_directory

app = Flask(__name__)

ARQUIVO_EXCEL = "malha_urbana.xlsx"
ARQUIVO_AUDIO = "freesound_community-loop-8-28783.mp3"

# Coeficientes multiplicadores de tempo para variáveis dinâmicas
CLIMAS = {"ensolarado": 1.0, "chuva_moderada": 1.25, "tempestade": 1.70}

CONDICOES_VIA = {"otima": 1.0, "buracos": 1.40, "obras_parciais": 2.00}


def criar_planilha_padrao_se_nao_existir():
    """Gera automaticamente o arquivo malha_urbana.xlsx caso ele nao exista."""
    if os.path.exists(ARQUIVO_EXCEL):
        return

    dados_vertices = [
        {"id_vertice": "N01", "tipo": "cruzamento", "nome": "Av. Central c/ R. 1", "bairro": "Centro", "pos_x": 350, "pos_y": 250},
        {"id_vertice": "N02", "tipo": "cruzamento", "nome": "Av. Central c/ Av. Brasil", "bairro": "Centro", "pos_x": 500, "pos_y": 250},
        {"id_vertice": "N03", "tipo": "cruzamento", "nome": "Pç. da Matriz c/ R. 1", "bairro": "Centro", "pos_x": 350, "pos_y": 350},
        {"id_vertice": "N04", "tipo": "cruzamento", "nome": "Pç. da Matriz c/ Av. Brasil", "bairro": "Centro", "pos_x": 500, "pos_y": 350},
        {"id_vertice": "N05", "tipo": "estabelecimento", "nome": "Farmácia Central", "bairro": "Centro", "pos_x": 420, "pos_y": 250},
        {"id_vertice": "N06", "tipo": "servico_publico", "nome": "Hospital Municipal", "bairro": "Centro", "pos_x": 520, "pos_y": 300},
        {"id_vertice": "N07", "tipo": "cruzamento", "nome": "R. das Palmeiras c/ R. 1", "bairro": "Norte", "pos_x": 350, "pos_y": 120},
        {"id_vertice": "N08", "tipo": "cruzamento", "nome": "R. das Palmeiras c/ Av. Brasil", "bairro": "Norte", "pos_x": 500, "pos_y": 120},
        {"id_vertice": "N09", "tipo": "escola", "nome": "Colégio Modelo", "bairro": "Norte", "pos_x": 300, "pos_y": 80},
        {"id_vertice": "N10", "tipo": "casa", "nome": "Condomínio Bela Vista", "bairro": "Norte", "pos_x": 580, "pos_y": 100},
        {"id_vertice": "N11", "tipo": "cruzamento", "nome": "R. das Flores c/ R. 1", "bairro": "Sul", "pos_x": 350, "pos_y": 480},
        {"id_vertice": "N12", "tipo": "cruzamento", "nome": "R. das Flores c/ Av. Brasil", "bairro": "Sul", "pos_x": 500, "pos_y": 480},
        {"id_vertice": "N13", "tipo": "cruzamento", "nome": "R. dos Cravos c/ R. das Flores", "bairro": "Sul", "pos_x": 650, "pos_y": 480},
        {"id_vertice": "N14", "tipo": "estabelecimento", "nome": "Supermercado Silva", "bairro": "Sul", "pos_x": 300, "pos_y": 480},
        {"id_vertice": "N15", "tipo": "casa", "nome": "Residência 42", "bairro": "Sul", "pos_x": 720, "pos_y": 480},
        {"id_vertice": "N16", "tipo": "casa", "nome": "Residência 108", "bairro": "Sul", "pos_x": 500, "pos_y": 560},
        {"id_vertice": "N17", "tipo": "cruzamento", "nome": "Av. Oeste c/ R. Palmeiras", "bairro": "Oeste", "pos_x": 150, "pos_y": 120},
        {"id_vertice": "N18", "tipo": "cruzamento", "nome": "Av. Oeste c/ Av. Central", "bairro": "Oeste", "pos_x": 150, "pos_y": 250},
        {"id_vertice": "N19", "tipo": "cruzamento", "nome": "Av. Oeste c/ R. Comércio", "bairro": "Oeste", "pos_x": 150, "pos_y": 400},
        {"id_vertice": "N20", "tipo": "estabelecimento", "nome": "Shopping Boulevard", "bairro": "Oeste", "pos_x": 100, "pos_y": 320},
        {"id_vertice": "N21", "tipo": "posto_combustivel", "nome": "Posto Shell Oeste", "bairro": "Oeste", "pos_x": 180, "pos_y": 220},
        {"id_vertice": "N22", "tipo": "cruzamento", "nome": "Av. Leste c/ R. Palmeiras", "bairro": "Leste", "pos_x": 700, "pos_y": 120},
        {"id_vertice": "N23", "tipo": "cruzamento", "nome": "Av. Leste c/ Av. Central", "bairro": "Leste", "pos_x": 700, "pos_y": 250},
        {"id_vertice": "N24", "tipo": "cruzamento", "nome": "Av. Leste c/ R. Cravos", "bairro": "Leste", "pos_x": 700, "pos_y": 400},
        {"id_vertice": "N25", "tipo": "estabelecimento", "nome": "Centro Médico Leste", "bairro": "Leste", "pos_x": 780, "pos_y": 250},
        {"id_vertice": "N26", "tipo": "cruzamento", "nome": "Trevo Rodovia Norte", "bairro": "Distrito Industrial", "pos_x": 350, "pos_y": 30},
        {"id_vertice": "N27", "tipo": "cruzamento", "nome": "Trevo Rodovia Leste", "bairro": "Distrito Industrial", "pos_x": 820, "pos_y": 120},
        {"id_vertice": "N28", "tipo": "centro_distribuicao", "nome": "CD Logístico Central", "bairro": "Distrito Industrial", "pos_x": 200, "pos_y": 30},
        {"id_vertice": "N29", "tipo": "industria", "nome": "Fábrica Metalúrgica", "bairro": "Distrito Industrial", "pos_x": 850, "pos_y": 60},
        {"id_vertice": "N30", "tipo": "posto_combustivel", "nome": "Posto Rodovia Sul", "bairro": "Sul", "pos_x": 350, "pos_y": 580}
    ]

    dados_arestas = [
        {"id_trecho": "A01", "origem": "N28", "destino": "N26", "nome_rua": "Rodovia Norte", "distancia_m": 350, "velocidade_max": 80, "sentido_padrao": "duplo"},
        {"id_trecho": "A02", "origem": "N26", "destino": "N07", "nome_rua": "Av. Perimetral Norte", "distancia_m": 250, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A03", "origem": "N26", "destino": "N27", "nome_rua": "Anel Rodoviário", "distancia_m": 600, "velocidade_max": 80, "sentido_padrao": "duplo"},
        {"id_trecho": "A04", "origem": "N27", "destino": "N29", "nome_rua": "R. Industrial", "distancia_m": 120, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A05", "origem": "N27", "destino": "N22", "nome_rua": "Alça Leste", "distancia_m": 220, "velocidade_max": 60, "sentido_padrao": "unico"},
        {"id_trecho": "A06", "origem": "N17", "destino": "N07", "nome_rua": "R. das Palmeiras (O)", "distancia_m": 400, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A07", "origem": "N07", "destino": "N08", "nome_rua": "R. das Palmeiras (C)", "distancia_m": 300, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A08", "origem": "N08", "destino": "N22", "nome_rua": "R. das Palmeiras (L)", "distancia_m": 400, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A09", "origem": "N07", "destino": "N09", "nome_rua": "Acesso Colégio", "distancia_m": 110, "velocidade_max": 30, "sentido_padrao": "duplo"},
        {"id_trecho": "A10", "origem": "N08", "destino": "N10", "nome_rua": "Acesso Condomínio", "distancia_m": 160, "velocidade_max": 30, "sentido_padrao": "unico"},
        {"id_trecho": "A11", "origem": "N17", "destino": "N18", "nome_rua": "Av. Oeste (Norte)", "distancia_m": 260, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A12", "origem": "N18", "destino": "N21", "nome_rua": "R. Posto Shell", "distancia_m": 70, "velocidade_max": 30, "sentido_padrao": "duplo"},
        {"id_trecho": "A13", "origem": "N18", "destino": "N01", "nome_rua": "Av. Central (Oeste)", "distancia_m": 400, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A14", "origem": "N01", "destino": "N05", "nome_rua": "R. do Comércio", "distancia_m": 140, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A15", "origem": "N05", "destino": "N02", "nome_rua": "Av. Central (Centro)", "distancia_m": 160, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A16", "origem": "N02", "destino": "N23", "nome_rua": "Av. Central (Leste)", "distancia_m": 400, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A17", "origem": "N23", "destino": "N25", "nome_rua": "Acesso Hospital Leste", "distancia_m": 160, "velocidade_max": 30, "sentido_padrao": "duplo"},
        {"id_trecho": "A18", "origem": "N07", "destino": "N01", "nome_rua": "R. Um (Norte)", "distancia_m": 260, "velocidade_max": 40, "sentido_padrao": "unico"},
        {"id_trecho": "A19", "origem": "N08", "destino": "N02", "nome_rua": "Av. Brasil (Norte)", "distancia_m": 260, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A20", "origem": "N22", "destino": "N23", "nome_rua": "Av. Leste (Norte)", "distancia_m": 260, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A21", "origem": "N01", "destino": "N03", "nome_rua": "R. Um (Centro)", "distancia_m": 200, "velocidade_max": 40, "sentido_padrao": "unico"},
        {"id_trecho": "A22", "origem": "N02", "destino": "N04", "nome_rua": "Av. Brasil (Centro)", "distancia_m": 200, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A23", "origem": "N02", "destino": "N06", "nome_rua": "R. Emergência Hospital", "distancia_m": 110, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A24", "origem": "N04", "destino": "N06", "nome_rua": "R. Traseira Hospital", "distancia_m": 110, "velocidade_max": 30, "sentido_padrao": "duplo"},
        {"id_trecho": "A25", "origem": "N03", "destino": "N04", "nome_rua": "Pç. da Matriz", "distancia_m": 300, "velocidade_max": 30, "sentido_padrao": "duplo"},
        {"id_trecho": "A26", "origem": "N18", "destino": "N19", "nome_rua": "Av. Oeste (Sul)", "distancia_m": 300, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A27", "origem": "N19", "destino": "N20", "nome_rua": "Acesso Shopping", "distancia_m": 180, "velocidade_max": 30, "sentido_padrao": "duplo"},
        {"id_trecho": "A28", "origem": "N19", "destino": "N11", "nome_rua": "R. Transversal Sul", "distancia_m": 420, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A29", "origem": "N03", "destino": "N11", "nome_rua": "R. Um (Sul)", "distancia_m": 260, "velocidade_max": 40, "sentido_padrao": "unico"},
        {"id_trecho": "A30", "origem": "N04", "destino": "N12", "nome_rua": "Av. Brasil (Sul)", "distancia_m": 260, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A31", "origem": "N14", "destino": "N11", "nome_rua": "Acesso Supermercado", "distancia_m": 100, "velocidade_max": 30, "sentido_padrao": "duplo"},
        {"id_trecho": "A32", "origem": "N11", "destino": "N12", "nome_rua": "R. das Flores (T1)", "distancia_m": 300, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A33", "origem": "N12", "destino": "N13", "nome_rua": "R. das Flores (T2)", "distancia_m": 300, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A34", "origem": "N13", "destino": "N15", "nome_rua": "R. dos Cravos (Residencial)", "distancia_m": 140, "velocidade_max": 30, "sentido_padrao": "unico"},
        {"id_trecho": "A35", "origem": "N13", "destino": "N24", "nome_rua": "R. dos Cravos (Leste)", "distancia_m": 200, "velocidade_max": 40, "sentido_padrao": "duplo"},
        {"id_trecho": "A36", "origem": "N23", "destino": "N24", "nome_rua": "Av. Leste (Sul)", "distancia_m": 300, "velocidade_max": 60, "sentido_padrao": "duplo"},
        {"id_trecho": "A37", "origem": "N12", "destino": "N16", "nome_rua": "R. das Açucenas", "distancia_m": 160, "velocidade_max": 30, "sentido_padrao": "unico"},
        {"id_trecho": "A38", "origem": "N11", "destino": "N30", "nome_rua": "Av. Radial Sul", "distancia_m": 200, "velocidade_max": 50, "sentido_padrao": "duplo"}
    ]

    with pd.ExcelWriter(ARQUIVO_EXCEL, engine="openpyxl") as writer:
        pd.DataFrame(dados_vertices).to_excel(writer, sheet_name="vertices", index=False)
        pd.DataFrame(dados_arestas).to_excel(writer, sheet_name="arestas", index=False)
    print(f"Planilha '{ARQUIVO_EXCEL}' gerada com sucesso.")


def carregar_malha():
    """Lê as abas 'vertices' e 'arestas' garantindo tipos de dados limpos e consistentes."""
    criar_planilha_padrao_se_nao_existir()

    df_v = pd.read_excel(
        ARQUIVO_EXCEL,
        sheet_name="vertices",
        dtype={"id_vertice": str, "tipo": str, "nome": str, "bairro": str}
    )
    df_a = pd.read_excel(
        ARQUIVO_EXCEL,
        sheet_name="arestas",
        dtype={"id_trecho": str, "origem": str, "destino": str, "nome_rua": str, "sentido_padrao": str}
    )

    # Limpeza de espaços em branco nos textos
    df_v["id_vertice"] = df_v["id_vertice"].astype(str).str.strip()
    df_v["tipo"] = df_v["tipo"].astype(str).str.strip().str.lower()
    df_v["nome"] = df_v["nome"].astype(str).str.strip()
    df_v["bairro"] = df_v["bairro"].astype(str).str.strip()
    df_v["pos_x"] = pd.to_numeric(df_v["pos_x"], errors="coerce").fillna(0.0)
    df_v["pos_y"] = pd.to_numeric(df_v["pos_y"], errors="coerce").fillna(0.0)

    df_a["origem"] = df_a["origem"].astype(str).str.strip()
    df_a["destino"] = df_a["destino"].astype(str).str.strip()
    df_a["nome_rua"] = df_a["nome_rua"].astype(str).str.strip()
    df_a["sentido_padrao"] = df_a["sentido_padrao"].astype(str).str.strip().str.lower()
    df_a["distancia_m"] = pd.to_numeric(df_a["distancia_m"], errors="coerce").fillna(100.0)
    df_a["velocidade_max"] = pd.to_numeric(df_a["velocidade_max"], errors="coerce").fillna(40.0)

    return df_v, df_a


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/audio/fundo")
def audio_fundo():
    """Entrega a trilha de fundo armazenada na raiz do projeto."""
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_AUDIO)


@app.route("/api/malha-inicial", methods=["GET"])
def malha_inicial():
    """Retorna os dados cadastrais fixos da planilha para alimentar a interface."""
    try:
        df_v, df_a = carregar_malha()

        nos = {
            row["id_vertice"]: {
                "x": float(row["pos_x"]),
                "y": float(row["pos_y"]),
                "nome": row["nome"],
                "tipo": row["tipo"],
                "bairro": row["bairro"]
            }
            for _, row in df_v.iterrows()
        }

        trechos = [
            {
                "origem": row["origem"],
                "destino": row["destino"],
                "bloqueado": False,
                "condicao": "otima",
                "rua": row["nome_rua"]
            }
            for _, row in df_a.iterrows()
        ]

        return jsonify({"status": "ok", "nos": nos, "trechos": trechos})

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route("/api/simular", methods=["POST"])
def simular():
    """Gera um cenário e executa o algoritmo de rota ótima (Dijkstra)."""
    dados_req = request.get_json(silent=True) or {}
    try:
        df_v, df_a = carregar_malha()
    except Exception as e:
        return jsonify({"status": "erro_planilha", "mensagem": str(e)}), 500

    G = nx.DiGraph()

    for _, row in df_v.iterrows():
        G.add_node(
            row["id_vertice"],
            tipo=row["tipo"],
            nome=row["nome"],
            bairro=row["bairro"],
            x=float(row["pos_x"]),
            y=float(row["pos_y"])
        )

    # Permite repetir um cenário pelo clima, mantendo o modo automático.
    clima_solicitado = dados_req.get("clima")
    clima_atual = clima_solicitado if clima_solicitado in CLIMAS else random.choice(list(CLIMAS.keys()))
    mult_clima = CLIMAS[clima_atual]
    trechos_info = []

    # 2. Construção dinâmica das arestas com variáveis estocásticas
    for _, row in df_a.iterrows():
        u = row["origem"]
        v = row["destino"]

        if u not in G or v not in G:
            continue

        dist = float(row["distancia_m"])
        vel = float(row["velocidade_max"])

        # 10% de probabilidade de via interditada/bloqueada
        bloqueado = random.random() < 0.10
        condicao = random.choices(["otima", "buracos", "obras_parciais"], weights=[0.70, 0.20, 0.10])[0]
        mult_condicao = CONDICOES_VIA[condicao]

        tempo_base = dist / (vel / 3.6)
        peso_final = (tempo_base * mult_clima * mult_condicao) if not bloqueado else float("inf")

        sentido = row["sentido_padrao"]
        # 5% de chance de inversão temporária de sentido por desvio
        if random.random() < 0.05:
            sentido = "invertido"

        direcoes = []
        if not bloqueado:
            if sentido == "duplo":
                direcoes = [(u, v), (v, u)]
            elif sentido == "unico":
                direcoes = [(u, v)]
            elif sentido == "invertido":
                direcoes = [(v, u)]

        for o, d in direcoes:
            G.add_edge(o, d, weight=peso_final)

        trechos_info.append({
            "origem": u,
            "destino": v,
            "bloqueado": bloqueado,
            "condicao": condicao,
            "rua": row["nome_rua"],
            "distancia_m": dist,
            "velocidade_max": vel
        })

    # 3. Leitura e validação dos pontos de origem e destino
    origem = dados_req.get("origem")
    destino = dados_req.get("destino")

    nos_disponiveis = list(G.nodes)
    if not nos_disponiveis:
        return jsonify({"status": "erro_planilha", "mensagem": "A planilha de vértices está vazia."})

    if origem not in G:
        origem = nos_disponiveis[0]
    if destino not in G:
        destino = nos_disponiveis[-1]

    # 4. Cálculo da rota e das métricas explicativas do Dijkstra
    rota = []
    custo_tempo = None
    status = "sucesso"
    distancias = {}

    try:
        distancias = nx.single_source_dijkstra_path_length(G, origem, weight="weight")
        rota = nx.dijkstra_path(G, origem, destino, weight="weight")
        custo_tempo = round(distancias[destino], 1)
    except nx.NetworkXNoPath:
        status = "sem_caminho"
    except Exception as e:
        status = f"erro: {str(e)}"

    nos_dict = {
        n: {
            "x": G.nodes[n]["x"],
            "y": G.nodes[n]["y"],
            "nome": G.nodes[n]["nome"],
            "tipo": G.nodes[n]["tipo"]
        }
        for n in G.nodes
    }

    trechos_bloqueados = sum(1 for trecho in trechos_info if trecho["bloqueado"])
    trechos_atencao = sum(1 for trecho in trechos_info if trecho["condicao"] != "otima")
    dijkstra_etapas = []
    custo_acumulado = 0.0
    for indice in range(len(rota) - 1):
        origem_etapa = rota[indice]
        destino_etapa = rota[indice + 1]
        custo_trecho = float(G[origem_etapa][destino_etapa]["weight"])
        custo_acumulado += custo_trecho
        dijkstra_etapas.append({
            "origem": origem_etapa,
            "destino": destino_etapa,
            "custo_trecho_s": round(custo_trecho, 1),
            "custo_acumulado_s": round(custo_acumulado, 1)
        })

    return jsonify({
        "status": status,
        "origem_usada": origem,
        "destino_usado": destino,
        "clima": clima_atual,
        "rota": rota,
        "tempo_estimado_s": custo_tempo,
        "dijkstra": {
            "algoritmo": "Dijkstra",
            "nos_alcancaveis": len(distancias),
            "arestas_avaliadas": G.number_of_edges(),
            "etapas": dijkstra_etapas
        },
        "metricas": {
            "total_trechos": len(trechos_info),
            "trechos_bloqueados": trechos_bloqueados,
            "trechos_atencao": trechos_atencao,
            "pontos_rota": len(rota)
        },
        "nos": nos_dict,
        "trechos": trechos_info
    })


if __name__ == "__main__":
    criar_planilha_padrao_se_nao_existir()
    app.run(debug=True, port=5000)