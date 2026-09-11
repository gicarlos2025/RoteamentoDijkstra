# RoteamentoDijkstra

MVP de um simulador de roteamento urbano baseado em grafos. A aplicação representa uma malha viária, simula condições dinâmicas de trânsito e calcula a rota de menor custo usando o algoritmo de Dijkstra.

## Funcionalidades

- Malha urbana com 30 pontos e 38 trechos.
- Geração automática da planilha `malha_urbana.xlsx` quando ela não existe.
- Seleção aleatória de origem e destino ao iniciar uma sessão.
- Cálculo automático de uma rota inicial.
- Seleção manual de origem, destino e cenário climático.
- Simulação de:
  - clima ensolarado;
  - chuva moderada;
  - tempestade;
  - trechos bloqueados;
  - buracos e obras parciais;
  - inversão temporária de sentido.
- Visualização da malha e da rota em Canvas.
- Animação do deslocamento do carro.
- Timeline animada dos pontos percorridos.
- Card visual com as etapas e os custos do algoritmo de Dijkstra.
- Música de fundo em loop, com volume inicial de 60%.
- Métricas de trechos, bloqueios, nós alcançáveis e custo acumulado.

## Tecnologias

- Python 3
- Flask
- NetworkX
- Pandas
- OpenPyXL
- HTML, CSS e JavaScript
- Canvas API

## Pré-requisitos

- Python 3.10 ou superior.
- PowerShell, Bash ou terminal equivalente.

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/gicarlos2025/RoteamentoDijkstra.git
cd RoteamentoDijkstra
```

Crie e ative o ambiente virtual:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências listadas no projeto:

```bash
python -m pip install -r requirements.txt
```

## Execução

Com o ambiente virtual ativado, execute:

```bash
python app.py
```

Abra no navegador:

```text
http://127.0.0.1:5000
```

No Windows, também é possível executar diretamente com o Python do ambiente virtual:

```powershell
.\.venv\Scripts\python.exe app.py
```

## Como usar

1. Aguarde a malha inicial carregar.
2. Uma origem, um destino e uma rota são escolhidos automaticamente.
3. Observe o grafo do Dijkstra e a animação do carro.
4. Altere origem, destino ou clima.
5. Clique em **Calcular Nova Rota** para gerar um novo cenário.
6. Passe o mouse sobre os pontos do mapa para consultar seus detalhes.

## API

### `GET /api/malha-inicial`

Retorna os nós e trechos fixos da malha urbana.

### `POST /api/simular`

Gera um cenário dinâmico e calcula a rota.

Exemplo de requisição:

```json
{
  "origem": "N28",
  "destino": "N15",
  "clima": "chuva_moderada"
}
```

Valores aceitos para `clima`:

- `automatico`
- `ensolarado`
- `chuva_moderada`
- `tempestade`

A resposta inclui o status da rota, o caminho encontrado, o tempo estimado, métricas da malha e as etapas explicativas do Dijkstra.

### `GET /audio/fundo`

Entrega a música de fundo usada pela interface.

## Estrutura do projeto

```text
RoteamentoDijkstra/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── freesound_community-loop-8-28783.mp3
├── LICENSE
├── .gitignore
└── malha_urbana.xlsx  # gerada localmente e ignorada pelo Git
```

## Observações

- A aplicação utiliza o servidor de desenvolvimento do Flask e está orientada para demonstração local.
- A cada simulação, bloqueios, condições das vias e sentidos podem mudar.
- O arquivo Excel é recriado automaticamente apenas quando não existe.
- O navegador pode exigir uma interação do usuário antes de liberar a reprodução automática do áudio.

## Licença

Consulte o arquivo [LICENSE](LICENSE) incluído no repositório.
