@startuml
!theme plain

actor "Cliente" as cliente
participant "Sistema de Caixa" as sistema
participant "Balança Digital" as balanca
participant "Câmera" as camera
participant "Serviço de IA\n(Reconhecimento)" as ia
database "Banco de Dados\nde Preços" as db

skinparam sequence {
    ArrowColor #555555
    ActorBorderColor #555555
    LifeLineBorderColor #555555
    ParticipantBorderColor #555555
    DatabaseBorderColor #555555
}

autonumber "<b>[0]"

cliente -> sistema: Coloca o produto na balança


sistema -> balanca: Requisitar peso estável
balanca --> sistema: Retorna o peso (ex: 0.5 kg)
    
sistema -> camera: Capturar imagem do produto
camera --> sistema: Retorna imagem
    
sistema -> ia: Analisar imagem para identificar o produto
ia --> sistema: Retorna o tipo do produto (ex: "Maçã")



sistema -> db: Consultar preço para "Maçã"
db --> sistema: Retorna preço por unidade/kg
    
sistema -> sistema: Calcula o preço final
    
sistema --> cliente: Exibe detalhes (Produto, Peso, Preço)


cliente -> sistema: Confirma a adição ou remoção\n do item ao carrinho

@enduml
