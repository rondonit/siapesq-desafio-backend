# SIAPESQ - Desafio Backend

Esse repositório contém o desafio técnico proposto para o processo seletivo para estagiário em desenvolvimento backend. O objetivo é consultar dados de espécies marítimas e variáveis de clima oceânico utilizando as APIs do GBIF e do Copernicus Marine Service.

## 1. Buscar ocorrências de espécies com `gbifer.py`
Execute o script `gbifer.py` para buscar ocorrências de determinada espécie utilizando a API do GBIF. Exemplo:

```bash
python3 gbifer.py --specie "thunnus obesus" --bbox 90 -90 180 -180 --limit 50 --begin_date '2016-01-01' --end_date '2021-02-01' --out_csv exemple.csv
```

*Args*:
    `--specie`: Nome científico da espécie
    `--bbox`: Coordenadas da caixa delimitadora no formato lat_max lat_min lon_max lon_min.
    `--limit`: Número máximo de ocorrências a retornar.
    `--begin_date`: Data inicial no formato YYYY-MM-DD.
    `--end_date`: Data final no formato YYYY-MM-DD.
    `--out_csv`: Nome do arquivo CSV de saída.

## 2. Consultar variáveis oceanográficas com o `dmarine.py`
Após gerar o CSV com o `gbifer.py`, use o script dmarine.py para consultar variáveis oceanográficas (como temperatura e salinidade) utilizando a API do Copernicus Marine. Exemplo:

```bash
python3 dmarine.py --csv exemple.csv --out_csv test.csv --max_workers=15
```
*Args*:
    - `--csv`: Nome do arquivo CSV de entrada (gerado pelo gbifer.py).
    - `--out_csv`: Nome do arquivo CSV de saída.
    - `--max_workers`: Número de threads para paralelizar as consultas (opcional, padrão: 5)

### Formato esperado do CSV de saída
O arquivo CSV gerado pelo dmarine.py deverá ter o seguinte formato:

```csv
decimalLongitude,decimalLatitude,year,day,month,thetao,so
76.510558,8.807378,2020,20,3,30.46830651909113,34.08764912746847
39.213491,-6.668138,2020,3,6,27.69893489778042,33.14767903648317
39.213491,-6.668138,2020,2,6,27.767784655094147,32.90963466279209
-81.982437,-1.827095,2020,10,10,22.890438549220562,33.75652329996228
114.86637,-33.99119,2020,13,10,19.643513292074203,35.65477458760142
153.344665,-27.312395,2018,28,12,25.436414681375027,35.83483379334211
-26.215975,37.567852,2017,22,8,24.254249699413776,36.37806326150894
35.56368,-23.8527,2016,7,3,28.93456830829382,34.52711566351354
35.45493,-21.48439,2016,11,3,31.071840561926365,20.636616088449955
35.56368,-23.8527,2016,6,4,27.96481215208769,35.39536725729704
35.56368,-23.8527,2016,5,5,26.669850759208202,35.22904138080776
35.56368,-23.8527,2016,25,10,25.54774620383978,35.28397469781339
```

## Lembretes
- Instale as dependências com `pip install -r requirements.txt`
- Configure as variáveis de ambiente no arquivo `.env` para autenticação na API do Copernicus Marine Service:
```
COPERNICUS_USER=<usuário>
COPERNICUS_PASS=<senha>
```