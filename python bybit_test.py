from pybit.unified_trading import HTTP
import time

# Configuração CORRETA da sessão
session = HTTP(
    api_key="MGnHwLr0JVgjvQttiJ",
    api_secret="UR9xpv0buDsJrQxQETrsCDcUXmXbxWP61JgY",
    recv_window=20000  # Janela de tempo ampliada
)

# Função para verificar sincronização
def verificar_tempo():
    try:
        # Obter tempo do servidor
        server_time = session.get_server_time()
        bybit_timestamp = int(server_time["result"]["timeSecond"]) * 1000
        
        # Tempo local
        local_timestamp = int(time.time() * 1000)
        
        # Calcular diferença
        diff = local_timestamp - bybit_timestamp
        print(f"Diferença de tempo: {diff}ms")
        return diff
        
    except Exception as e:
        print(f"Erro na sincronização: {e}")
        return None

# Executar verificação
diff = verificar_tempo()

# Exemplo de uso correto (buscar preço BTC)
if diff is not None and abs(diff) < 3000:  # Tolerância de 3 segundos
    try:
        preco = session.get_tickers(category="linear", symbol="BTCUSDT")
        print("Preço:", preco["result"]["list"][0]["lastPrice"])
    except Exception as e:
        print(f"Erro na requisição: {e}")
else:
    print("Erro: Relógio dessincronizado. Ajuste o horário do sistema!")