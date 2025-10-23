# Relatório de Testes de Funcionalidade: Holopad

## Teste #1: Iluminação Ideal (Solar)

**Condições:** Varanda com janelas de vidro à tarde (luz solar difusa).
**Luminosidade (Lux):** `624 Lux`

| Funcionalidade | Resultado | Observações |
| :--- | :---: | :--- |
| **Detecção Geral** | Ótimo | Detecção imediata e 100% estável (sem "jitter"). |
| **Apontar (Mover)** | Ótimo | Movimento perfeitamente fluido e responsivo. |
| **Feedback Visual** | OK | Todas as cores de estado (Azul, Amarelo, Vermelho) corresponderam. |
| **Clique Esquerdo** | Ótimo (10/10) | Precisão total, sem falsos positivos. |
| **Congelamento (Freeze)**| Ótimo | Congelou no momento exato da intenção de clique. |
| **Arrastar (Drag)** | Ótimo | Manteve o clique pressionado sem falhas. |
| **Clique Direito** | Ótimo (10/10) | Gesto distinto, sem conflitos. |
| **Scroll (3 Dedos)** | Ótimo | Detecção imediata, rolagem suave. |
| **Gesto de Parar** | Imediato | Funcionou na primeira tentativa. |

### Resumo Geral do Teste #1
**Análise:** Condição de iluminação perfeita. O modelo operou com máxima performance, precisão e responsividade em todas as funcionalidades.
**Conclusão:** ✅ **Usável**

---

## Teste #2: Iluminação Interna (Boa)

**Condições:** Sala bem iluminada (luz central acesa e janelas abertas).
**Luminosidade (Lux):** `137 Lux`

| Funcionalidade | Resultado | Observações |
| :--- | :---: | :--- |
| **Detecção Geral** | Ótimo | Detecção imediata e estável. |
| **Apontar (Mover)** | Bom | Leve latência ("lag") perceptível, mas totalmente funcional. |
| **Feedback Visual** | OK | Todas as cores de estado funcionaram. |
| **Clique Esquerdo** | Bom (>7/10) | **Falsos positivos (cliques não intencionais) ocorreram esporadicamente.** |
| **Congelamento (Freeze)**| Ótimo | Funcionou como esperado. |
| **Arrastar (Drag)** | Bom | **Atraso notável para *iniciar* o gesto de arrastar**, mas manteve. |
| **Clique Direito** | Bom (>7/10) | Precisão boa, sem conflitos. |
| **Scroll (3 Dedos)** | Ótimo | Detecção imediata e suave. |
| **Gesto de Parar** | Imediato | Funcionou na primeira tentativa. |

### Resumo Geral do Teste #2
**Análise:** Iluminação interna muito boa. O desempenho geral continua excelente, mas com uma leve queda na responsividade (latência) e na precisão do clique.
**Conclusão:** ✅ **Usável**

---

## Teste #3: Iluminação Interna (Padrão)

**Condições:** Quarto com a luz central acesa (sem luz solar).
**Luminosidade (Lux):** `43 Lux`

| Funcionalidade | Resultado | Observações |
| :--- | :---: | :--- |
| **Detecção Geral** | Ótimo | Detecção imediata e estável. |
| **Apontar (Mover)** | Bom | Leve latência, similar ao Teste #2. |
| **Feedback Visual** | OK | Todas as cores de estado funcionaram. |
| **Clique Esquerdo** | Bom (>7/10) | Falsos positivos ocorreram esporadicamente (similar ao Teste #2). |
| **Congelamento (Freeze)**| Ótimo | Funcionou como esperado. |
| **Arrastar (Drag)** | Bom | Atraso notável para iniciar o gesto (similar ao Teste #2). |
| **Clique Direito** | Bom (>7/10) | Precisão boa, sem conflitos. |
| **Scroll (3 Dedos)** | Ótimo | Detecção imediata e suave. |
| **Gesto de Parar** | Imediato | Funcionou na primeira tentativa. |

### Resumo Geral do Teste #3
**Análise:** O desempenho foi funcionalmente idêntico ao Teste #2, sugerindo que `~40 Lux` ainda é suficiente para uma operação robusta.
**Conclusão:** ✅ **Usável**

---

## Teste #4: Iluminação Baixa (Lâmpada)

**Condições:** Quarto escuro com uma lâmpada (abajur) ligada.
**Luminosidade (Lux):** `5 Lux`

| Funcionalidade | Resultado | Observações |
| :--- | :---: | :--- |
| **Detecção Geral** | Ruim | Detecção imediata, mas com **"jitter" (tremor) leve** constante. |
| **Apontar (Mover)** | Ruim | **Latência significativa**, dificultando o controle fino. |
| **Feedback Visual** | Ruim | As cores de estado atualizavam, mas com atraso visível. |
| **Clique Esquerdo** | Ruim (<7/10) | Alta taxa de falsos positivos. |
| **Congelamento (Freeze)**| Ruim | Atraso perceptível para congelar o cursor. |
| **Arrastar (Drag)** | Bom | Funcionou, mas **soltou o clique involuntariamente** algumas vezes. |
| **Clique Direito** | Ruim (<7/10) | **Conflito de Gesto:** Confundiu o clique direito com o gesto de 'Scroll'. |
| **Scroll (3 Dedos)** | Ruim | Detecção imediata, mas a rolagem foi lenta e travada. |
| **Gesto de Parar** | Imediato | Funcionou. (Ver Análise). |

### Resumo Geral do Teste #4
**Análise:** Desempenho severamente degradado. A baixa luz causou "jitter" e alta latência.
**Bug Crítico:** Ocorreram conflitos de gestos, principalmente o modelo interpretando cliques/scrolls como o gesto de "Parar", forçando a reinicialização do programa.
**Conclusão:** ⚠️ **Usável com dificuldade**

---

## Teste #5: Iluminação Extrema (Monitor)

**Condições:** Quarto escuro, apenas com a iluminação do monitor.
**Luminosidade (Lux):** `1 Lux`

| Funcionalidade | Resultado | Observações |
| :--- | :---: | :--- |
| **Detecção Geral** | Falha | A mão foi detectada inicialmente. |
| **Todos os Gestos** | Falha | Qualquer gesto (apontar, clicar, etc.) foi interpretado erroneamente como o gesto de "Parar". |

### Resumo Geral do Teste #5
**Análise:** Falha crítica e total. O modelo não consegue distinguir landmarks com eficácia, interpretando qualquer movimento como o gesto de punho fechado ("Parar"). O programa encerrava imediatamente ao tentar qualquer interação.
**Conclusão:** ❌ **Inutilizável**