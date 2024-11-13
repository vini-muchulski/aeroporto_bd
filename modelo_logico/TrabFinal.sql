/* modelo_logico2: */

CREATE TABLE Passageiro (
    codigo_passageiro INTEGER PRIMARY KEY,
    nome VARCHAR,
    documento VARCHAR,
    contato VARCHAR
);

CREATE TABLE Bilhete_Voo (
    numero_bilhete INTEGER PRIMARY KEY,
    classe INTEGER,
    nome_passageiro VARCHAR,
    status VARCHAR
);

CREATE TABLE Voo (
    numero_voo INTEGER PRIMARY KEY,
    origem VARCHAR,
    destino VARCHAR,
    horario_chegada VARCHAR,
    horario_partida VARCHAR
);

CREATE TABLE Aeronave (
    prefixo_aeronave VARCHAR PRIMARY KEY,
    modelo VARCHAR,
    capacidade INTEGER
);

CREATE TABLE Portao_Embarque (
    codigo_portao INTEGER PRIMARY KEY,
    localizacao VARCHAR,
    status VARCHAR
);

CREATE TABLE Companhia_Aerea (
    codigo_companhia INTEGER PRIMARY KEY,
    nome VARCHAR,
    pais VARCHAR
);

CREATE TABLE Area_Bagagem (
    codigo_bagagem INTEGER PRIMARY KEY,
    status VARCHAR
);

CREATE TABLE Controle_Seguranca (
    codigo_seguranca INTEGER PRIMARY KEY,
    inspecao VARCHAR,
    status VARCHAR
);

CREATE TABLE Funcionario (
    id_funcionario INTEGER PRIMARY KEY,
    nome VARCHAR,
    cargo VARCHAR,
    setor VARCHAR
);

CREATE TABLE Servicoes_AeroPortuarios (
    codigo_servico INTEGER PRIMARY KEY,
    descricao VARCHAR
);

CREATE TABLE Compra (
    fk_Passageiro_codigo_passageiro INTEGER,
    fk_Bilhete_Voo_numero_bilhete INTEGER
);

CREATE TABLE Passa_por (
    fk_Passageiro_codigo_passageiro INTEGER,
    fk_Controle_Seguranca_codigo_seguranca INTEGER
);

CREATE TABLE Realiza (
    fk_Funcionario_id_funcionario INTEGER,
    fk_Servicoes_AeroPortuarios_codigo_servico INTEGER
);

CREATE TABLE Despacha (
    fk_Passageiro_codigo_passageiro INTEGER,
    fk_Area_Bagagem_codigo_bagagem INTEGER
);

CREATE TABLE esta_associado_a (
    fk_Voo_numero_voo INTEGER,
    fk_Area_Bagagem_codigo_bagagem INTEGER
);

CREATE TABLE é_operado_por (
    fk_Voo_numero_voo INTEGER,
    fk_Companhia_Aerea_codigo_companhia INTEGER
);

CREATE TABLE usa (
    fk_Voo_numero_voo INTEGER,
    fk_Portao_Embarque_codigo_portao INTEGER
);

CREATE TABLE usava (
    fk_Aeronave_prefixo_aeronave VARCHAR,
    fk_Voo_numero_voo INTEGER
);

CREATE TABLE relaciona_se (
    fk_Bilhete_Voo_numero_bilhete INTEGER,
    fk_Voo_numero_voo INTEGER
);
 
ALTER TABLE Compra ADD CONSTRAINT FK_Compra_1
    FOREIGN KEY (fk_Passageiro_codigo_passageiro)
    REFERENCES Passageiro (codigo_passageiro)
    ON DELETE SET NULL;
 
ALTER TABLE Compra ADD CONSTRAINT FK_Compra_2
    FOREIGN KEY (fk_Bilhete_Voo_numero_bilhete)
    REFERENCES Bilhete_Voo (numero_bilhete)
    ON DELETE SET NULL;
 
ALTER TABLE Passa_por ADD CONSTRAINT FK_Passa_por_1
    FOREIGN KEY (fk_Passageiro_codigo_passageiro)
    REFERENCES Passageiro (codigo_passageiro)
    ON DELETE SET NULL;
 
ALTER TABLE Passa_por ADD CONSTRAINT FK_Passa_por_2
    FOREIGN KEY (fk_Controle_Seguranca_codigo_seguranca)
    REFERENCES Controle_Seguranca (codigo_seguranca)
    ON DELETE SET NULL;
 
ALTER TABLE Realiza ADD CONSTRAINT FK_Realiza_1
    FOREIGN KEY (fk_Funcionario_id_funcionario)
    REFERENCES Funcionario (id_funcionario)
    ON DELETE SET NULL;
 
ALTER TABLE Realiza ADD CONSTRAINT FK_Realiza_2
    FOREIGN KEY (fk_Servicoes_AeroPortuarios_codigo_servico)
    REFERENCES Servicoes_AeroPortuarios (codigo_servico)
    ON DELETE SET NULL;
 
ALTER TABLE Despacha ADD CONSTRAINT FK_Despacha_1
    FOREIGN KEY (fk_Passageiro_codigo_passageiro)
    REFERENCES Passageiro (codigo_passageiro)
    ON DELETE SET NULL;
 
ALTER TABLE Despacha ADD CONSTRAINT FK_Despacha_2
    FOREIGN KEY (fk_Area_Bagagem_codigo_bagagem)
    REFERENCES Area_Bagagem (codigo_bagagem)
    ON DELETE SET NULL;
 
ALTER TABLE esta_associado_a ADD CONSTRAINT FK_esta_associado_a_1
    FOREIGN KEY (fk_Voo_numero_voo)
    REFERENCES Voo (numero_voo)
    ON DELETE SET NULL;
 
ALTER TABLE esta_associado_a ADD CONSTRAINT FK_esta_associado_a_2
    FOREIGN KEY (fk_Area_Bagagem_codigo_bagagem)
    REFERENCES Area_Bagagem (codigo_bagagem)
    ON DELETE SET NULL;
 
ALTER TABLE é_operado_por ADD CONSTRAINT FK_é_operado_por_1
    FOREIGN KEY (fk_Voo_numero_voo)
    REFERENCES Voo (numero_voo)
    ON DELETE SET NULL;
 
ALTER TABLE é_operado_por ADD CONSTRAINT FK_é_operado_por_2
    FOREIGN KEY (fk_Companhia_Aerea_codigo_companhia)
    REFERENCES Companhia_Aerea (codigo_companhia)
    ON DELETE SET NULL;
 
ALTER TABLE usa ADD CONSTRAINT FK_usa_1
    FOREIGN KEY (fk_Voo_numero_voo)
    REFERENCES Voo (numero_voo)
    ON DELETE SET NULL;
 
ALTER TABLE usa ADD CONSTRAINT FK_usa_2
    FOREIGN KEY (fk_Portao_Embarque_codigo_portao)
    REFERENCES Portao_Embarque (codigo_portao)
    ON DELETE SET NULL;
 
ALTER TABLE usava ADD CONSTRAINT FK_usava_1
    FOREIGN KEY (fk_Aeronave_prefixo_aeronave)
    REFERENCES Aeronave (prefixo_aeronave)
    ON DELETE SET NULL;
 
ALTER TABLE usava ADD CONSTRAINT FK_usava_2
    FOREIGN KEY (fk_Voo_numero_voo)
    REFERENCES Voo (numero_voo)
    ON DELETE SET NULL;
 
ALTER TABLE relaciona_se ADD CONSTRAINT FK_relaciona_se_1
    FOREIGN KEY (fk_Bilhete_Voo_numero_bilhete)
    REFERENCES Bilhete_Voo (numero_bilhete)
    ON DELETE SET NULL;
 
ALTER TABLE relaciona_se ADD CONSTRAINT FK_relaciona_se_2
    FOREIGN KEY (fk_Voo_numero_voo)
    REFERENCES Voo (numero_voo)
    ON DELETE SET NULL;