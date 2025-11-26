DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS unidades;

DROP TABLE IF EXISTS invoices;

CREATE TABLE invoices (
    id int NOT NULL AUTO_INCREMENT,
    invoice_type varchar(3) NOT NULL DEFAULT 'N\D',
    invoice_number varchar(50) NOT NULL,
    issue_date date DEFAULT NULL,
    taxpayer_number varchar(20) DEFAULT NULL,
    account_number varchar(20) DEFAULT NULL,
    client varchar(255) NOT NULL,
    address longtext,
    cvp varchar(12) DEFAULT NULL,
    invoice_period_month varchar(20) DEFAULT NULL,
    invoice_period_year varchar(4) DEFAULT NULL,
    total_amount decimal(10, 2) DEFAULT NULL,
    amount_to_pay decimal(10, 2) DEFAULT NULL,
    sent_validar tinyint(1) DEFAULT '0',
    quitar tinyint(1) DEFAULT '0',
    quita_date datetime DEFAULT NULL,
    pdffile varchar(255) DEFAULT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE unidades (
    id int NOT NULL AUTO_INCREMENT,
    num_cliente varchar(50) NOT NULL,
    unidade varchar(100) NOT NULL,
    poc varchar(100) DEFAULT NULL,
    email_poc varchar(100) DEFAULT NULL,
    created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_num_cliente_unidade (num_cliente, unidade)
);

CREATE TABLE users (
    id int NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    display_name varchar(255) DEFAULT NULL,
    email varchar(255) DEFAULT NULL,
    is_admin tinyint(1) DEFAULT '0',
    last_login timestamp NULL DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username)
);

INSERT INTO
    invoices (
        invoice_number,
        issue_date,
        taxpayer_number,
        account_number,
        client,
        address,
        cvp,
        invoice_period_month,
        invoice_period_year,
        total_amount,
        amount_to_pay,
        sent_validar,
        quitar,
        quita_date,
        pdffile
    )
VALUES (
        '579119200',
        '2025-02-04',
        '600012662',
        '1461369171',
        'NRP CASSIOPEIA',
        'BLOCO A<br>SI BASE NAVAL ALFEITE SN<br>ALMADA<br>2810-001 ALMADA',
        '202682626622',
        'fevereiro',
        '2025',
        0.46,
        0.46,
        0,
        1,
        '2025-04-30 07:51:17',
        '2025PT504615947009296_VISAO-FORNECEDOR.pdf'
    ),
    (
        '579119146',
        '2025-02-04',
        '600012662',
        '1407769051',
        'NRP ARPÃO',
        'BLOCO A<br>SI BASE NAVAL ALFEITE BNL MDN<br>ALMADA<br>2810-001 ALMADA',
        '202682626622',
        'fevereiro',
        '2025',
        2.38,
        2.38,
        0,
        1,
        '2025-04-30 07:51:17',
        '2025PT504615947008445_VISAO-FORNECEDOR.pdf'
    ),
    (
        '579119191',
        '2025-02-04',
        '600012662',
        '1486769050',
        'NRP SAGRES',
        'BLOCO A<br>SI BASE NAVAL ALFEITE SN<br>ALMADA<br>2810-001 ALMADA',
        '202682626622',
        'fevereiro',
        '2025',
        1.26,
        1.26,
        0,
        1,
        '2025-04-30 07:51:17',
        '2025PT504615947008530_VISAO-FORNECEDOR.pdf'
    ),
    (
        '579119188',
        '2025-02-04',
        '600012662',
        '1455269174',
        'ESQUADRILHA DE SUBSUPERFICIE',
        'BLOCO A<br>SI BASE NAVAL ALFEITE SN<br>ALMADA<br>2810-001 ALMADA',
        '202682626622',
        'fevereiro',
        '2025',
        2.61,
        2.61,
        0,
        1,
        '2025-04-30 07:51:17',
        '2025PT504615947008528_VISAO-FORNECEDOR.pdf'
    ),
    (
        '579119143',
        '2025-02-04',
        '600012662',
        '1463869053',
        'DIRECÇÃO DE ABASTECIMENTO',
        'BLOCO A<br>SI BASE NAVAL ALFEITE BNL MDN<br>ALMADA<br>2810-001 ALMADA',
        '202682626622',
        'fevereiro',
        '2025',
        12.73,
        12.73,
        0,
        1,
        '2025-04-30 07:51:17',
        '2025PT504615947008524_VISAO-FORNECEDOR.pdf'
    );

INSERT INTO
    unidades (
        num_cliente,
        unidade,
        poc,
        email_poc,
        created_at,
        updated_at
    )
VALUES (
        '1466769058',
        'GABINETE DO CEMA',
        '1SAR FZ Coelho Lobão',
        'coelho.lobao@marinha.pt',
        '2025-03-29 21:15:12',
        '2025-04-30 14:14:50'
    ),
    (
        '1494062899',
        'COMNAV',
        'CTEN STP Ramos Silveiro',
        'ramos.silveiro@marinha.pt',
        '2025-04-30 13:30:36',
        '2025-04-30 14:57:44'
    ),
    (
        '1494263296',
        'COMNAV',
        'CTEN STP Ramos Silveiro',
        'ramos.silveiro@marinha.pt',
        '2025-04-30 13:31:08',
        '2025-04-30 14:58:15'
    ),
    (
        '1468769056',
        'CHEFIA DE ASSISTÊNCIA RELIGIOSA DA MARINHA',
        'CAB R Dionísio da Rocha',
        'dionisio.rocha@marinha.pt',
        '2025-04-30 13:35:02',
        '2025-04-30 13:35:02'
    ),
    (
        '1465769052',
        'DIREÇÃO DE APOIO  SOCIAL',
        'TEC INF Gracinda Gomes Ferreira',
        'gracinda.maria.ferreira@marinha.pt',
        '2025-04-30 13:36:13',
        '2025-04-30 13:36:13'
    ),
    (
        '1472670835',
        'UNIDADE DE APOIO ÀS INSTALAÇÕES CENTRAIS DE MARINHA',
        'SAJ C Almeida Sousa',
        'uaicm.sec.inf.com@marinha.pt',
        '2025-04-30 13:37:15',
        '2025-04-30 13:37:15'
    ),
    (
        '1451369170',
        'SF - GABINETE DO SUPERINTENDENTE',
        'ESP.INF. GR.3 NI.1 Amaral Pereira',
        'amaral.pereira@marinha.pt',
        '2025-04-30 13:38:42',
        '2025-04-30 13:38:42'
    ),
    (
        '1426269185',
        'SF - DIREÇÃO ADMINISTRAÇÃO FINANCEIRA',
        'ESP.INF. GR.3 NI.1 Amaral Pereira',
        'amaral.pereira@marinha.pt',
        '2025-04-30 13:39:21',
        '2025-04-30 13:39:21'
    ),
    (
        '1466269188',
        'SF - DIRECÇÃO DE CONTABILIDADE E OPERAÇÕES FINANCEIRAS',
        'ESP.INF. GR.3 NI.1 Amaral Pereira',
        'amaral.pereira@marinha.pt',
        '2025-04-30 13:40:06',
        '2025-04-30 13:40:06'
    ),
    (
        '1458269189',
        'SF - DIRECÇÃO DE CONTROLO FINANCEIRO',
        'ESP.INF. GR.3 NI.1 Amaral Pereira',
        'amaral.pereira@marinha.pt',
        '2025-04-30 13:41:03',
        '2025-04-30 13:41:03'
    ),
    (
        '1435269181',
        'NRP  SAGITARIO',
        '1TEN M Mira Pinhão',
        'mira.pinhao@marinha.pt',
        '2025-04-30 13:42:31',
        '2025-04-30 13:42:31'
    ),
    (
        '1446769054',
        'NRP  ESCORPIAO',
        '1TEN M Paredes Bezerra',
        'nrpescorpiao.comandante@marinha.pt',
        '2025-04-30 13:44:52',
        '2025-04-30 13:44:52'
    ),
    (
        '1433369176',
        'NRP SETÚBAL',
        'GMAR EN-AEL Beirão Amador',
        'beirao.amador@marinha.pt',
        '2025-04-30 13:46:12',
        '2025-04-30 13:46:12'
    ),
    (
        '1457269171',
        'NRP  HIDRA',
        '2TEN M Zegre Parreira',
        'nrphidra.comandante@marinha.pt',
        '2025-04-30 13:47:01',
        '2025-04-30 13:47:01'
    ),
    (
        '1448069631',
        'DIREÇÃO DE FORMAÇÃO',
        'CMG M Moreira Silva',
        'df.dir@marinha.pt',
        '2025-04-30 13:47:55',
        '2025-04-30 13:47:55'
    ),
    (
        '1456670688',
        'ESCOLA NAVAL',
        'CFR M Silva Precioso',
        'silva.precioso@marinha.pt',
        '2025-04-30 13:48:57',
        '2025-04-30 13:48:57'
    ),
    (
        '1494263296',
        'CÉLULA DE EXPERIMENTAÇÃO OPERACIONAL DE VEÍCULOS NÃO TRÍPULADOS',
        '2TEN M Rocha Araújo',
        'rocha.araujo@marinha.pt',
        '2025-04-30 13:51:51',
        '2025-04-30 13:51:51'
    ),
    (
        '1407769050',
        'ESCOLA DE  FUZILEIROS',
        'SAJ C Pinto da Rocha',
        'cf.bf.scomms.centro.adj@marinha.pt',
        '2025-04-30 13:53:22',
        '2025-04-30 13:53:22'
    ),
    (
        '1402369179',
        'NRP  PÉGASO',
        '2TEN M Luís Ferreira',
        'luis.ferreira@marinha.pt',
        '2025-04-30 13:54:29',
        '2025-04-30 13:54:29'
    ),
    (
        '1450369174',
        'NRP FIGUEIRA DA FOZ',
        'GMAR EN-AEL Nunes Rodrigues',
        'francisco.nunes.rodrigues@marinha.pt',
        '2025-04-30 13:55:11',
        '2025-04-30 13:55:11'
    ),
    (
        '1465269171',
        'NRP  RIO MINHO',
        '2TEN M MARTIN FEDORCHUCK',
        'nrpriominho.comandante@marinha.pt',
        '2025-04-30 13:56:02',
        '2025-04-30 13:56:02'
    ),
    (
        '1419770173',
        'NRP POLAR',
        '2TEN M Dinis da Silva',
        'nrppolar.imediato@marinha.pt',
        '2025-04-30 13:56:36',
        '2025-04-30 13:56:36'
    ),
    (
        '1431469620',
        'NRP  ZAIRE',
        '2TEN M Leal Oliveira',
        'nrpzaire.imediato@marinha.pt',
        '2025-04-30 13:57:09',
        '2025-04-30 13:57:09'
    ),
    (
        '1451071301',
        'NRP SINES',
        'GMAR EN-AEL Cardoso Lopes',
        'm1x3623101@marinha.pt',
        '2025-04-30 14:00:13',
        '2025-04-30 14:00:13'
    ),
    (
        '1482369175',
        'NRP  DRAGÃO',
        '2TEN M Afonso Ramos',
        'afonso.ramos@marinha.pt',
        '2025-04-30 14:01:53',
        '2025-04-30 14:01:53'
    ),
    (
        '1486769050',
        'NRP  SAGRES',
        '2TEN EN-AEL Caldeira Chaves',
        'nrpsagres.2301@marinha.pt',
        '2025-04-30 14:02:25',
        '2025-04-30 14:02:25'
    ),
    (
        '1446269184',
        'NRP ANTÓNIO  ENES',
        'GMAR EN-AEL Correia Gonçalves',
        'nrpaenes.2301@marinha.pt',
        '2025-04-30 14:03:01',
        '2025-04-30 14:03:01'
    ),
    (
        '1480369178',
        'NRP  ANDROMEDA',
        '2TEN M Alves Ratinho',
        'alves.ratinho@marinha.pt',
        '2025-04-30 14:03:45',
        '2025-04-30 14:03:45'
    ),
    (
        '1436269174',
        'NRP  ORION',
        '2TEN M Farinha Martins',
        'nrporion.comandante@marinha.pt',
        '2025-04-30 14:04:43',
        '2025-04-30 14:04:43'
    ),
    (
        '1458269188',
        'NRP TEJO',
        '2TEN M Rosa Pires',
        'nrptejo.comandante@marinha.pt',
        '2025-04-30 14:05:29',
        '2025-04-30 14:05:29'
    ),
    (
        '1435269186',
        'NRP VIANA DO CASTELO',
        'GMAR EN-AEL Matilde Correia Vieira',
        'nrpvcastelo.3101@marinha.pt',
        '2025-04-30 14:06:02',
        '2025-04-30 14:06:02'
    ),
    (
        '1468071272',
        'ESCOLA DE TECNOLOGIAS NAVAIS',
        '2TEN EN-AEL Coelho Lourenço',
        'etna.ch.infor@marinha.pt',
        '2025-04-30 14:07:00',
        '2025-04-30 14:07:00'
    ),
    (
        '1476769050',
        'NRP  D CARLOS I',
        'GMAR EN-AEL KITCHECANAR GOMES',
        'kitchecanar.gomes@marinha.pt',
        '2025-04-30 14:07:53',
        '2025-04-30 14:07:53'
    ),
    (
        '1437769056',
        'CENTRO INTEGRADO DE TREINO E AVALIAÇÃO NAVAL',
        'CTEN EN-AEL Rodrigues Quitério',
        'rodrigues.quiterio@marinha.pt',
        '2025-04-30 14:08:55',
        '2025-04-30 14:08:55'
    ),
    (
        '1406269181',
        'NRP BARTOLOMEU DIAS',
        '2TEN EN-AEL DMYTRO YANTSUR',
        'nrpbdias.3101@marinha.pt',
        '2025-04-30 14:09:36',
        '2025-04-30 14:09:36'
    ),
    (
        '1405269182',
        'NRP ALM GAGO COUTINHO',
        'CFR EN-MEC Oliveira Azenha',
        'oliveira.azenha@marinha.pt',
        '2025-04-30 14:10:12',
        '2025-04-30 14:10:12'
    ),
    (
        '1436269186',
        'NRP DOURO',
        'CFR EN-MEC Oliveira Azenha',
        'oliveira.azenha@marinha.pt',
        '2025-04-30 14:11:02',
        '2025-04-30 14:11:02'
    ),
    (
        '1456269189',
        'NRP ZARCO',
        '2TEN EN-AEL Ferreira Maia',
        'nrpzarco.imediato@marinha.pt',
        '2025-04-30 14:11:41',
        '2025-04-30 14:11:41'
    ),
    (
        '1482869050',
        'MESSE MARINHA CASCAIS',
        'CMOR AD GOMES GRAVE',
        'gomes.grave@marinha.pt',
        '2025-04-30 14:12:28',
        '2025-04-30 14:12:28'
    ),
    (
        '1453269832',
        'ACADEMIA DE MARINHA',
        'CAB V Roldão Mendes',
        'academiamarinha.sec@marinha.pt',
        '2025-04-30 14:15:16',
        '2025-04-30 14:15:16'
    ),
    (
        '1481369176',
        'DIRECÇÃO  DE TRANSPORTES',
        'MAQ 1CL Louro Alvarinho',
        'dt.informatica@marinha.pt',
        '2025-04-30 14:16:17',
        '2025-04-30 14:16:17'
    ),
    (
        '1455269174',
        'ESQUADRILHA DE SUBSUPERFICIE',
        'SAJ ETI Correia Felgueiras',
        'drisubadu@marinha.pt',
        '2025-04-30 14:17:44',
        '2025-04-30 14:17:44'
    ),
    (
        '1483269170',
        'DIREÇÃO DE SAÚDE',
        '1TEN TS Afonso Nobre',
        'ds.chefe.sa@marinha.pt',
        '2025-04-30 14:18:37',
        '2025-04-30 14:18:37'
    ),
    (
        '1466969879',
        'CENTRO DE EDUCAÇÃO FÍSICA DA ARMADA',
        '1SAR L Dias Coelho',
        'cefa.sag.sgfp.ch@marinha.pt',
        '2025-04-30 14:19:35',
        '2025-04-30 14:19:35'
    ),
    (
        '1466769056',
        'BASE NAVAL LISBOA',
        'SCH ETA Santos Gomes',
        'm3a020117@marinha.pt',
        '2025-04-30 14:21:00',
        '2025-04-30 14:21:00'
    ),
    (
        '1441969852',
        'COMANDO DA ZONA MARITIMA DO NORTE',
        '1SAR B Fernandes Sampaio',
        'czmnorte.adu@marinha.pt',
        '2025-04-30 14:21:43',
        '2025-04-30 14:21:43'
    ),
    (
        '1458769053',
        'COMANDO DA ZONA MARITIMA DA MADEIRA',
        'SAJ ETC Redondo Ferreira',
        'czmm_adu@marinha.pt',
        '2025-04-30 14:22:28',
        '2025-04-30 14:22:28'
    ),
    (
        '1461770680',
        'COMANDO ZONA MARITIMA DO SUL',
        'SAJ ETI Duarte Lourenço',
        'duarte.lourenco@marinha.pt',
        '2025-04-30 14:24:37',
        '2025-04-30 14:24:37'
    ),
    (
        '1435769053',
        'DIREÇÃO CULTURAL DA  MARINHA',
        'SAJ A Teixeira do Nascimento',
        'dcm.admin.redes.si@marinha.pt',
        '2025-04-30 14:25:31',
        '2025-04-30 14:25:31'
    ),
    (
        '1446269182',
        'SUPERINTENDÊNCIA DO MATERIAL',
        'CMOR L Pinto Mendes',
        'sm.saf@marinha.pt',
        '2025-04-30 14:26:20',
        '2025-04-30 14:26:20'
    ),
    (
        '1444269182',
        'SUPERINTENDÊNCIA DO PESSOAL',
        'CFR STP Santos Dias',
        'sp.ssi.ch@marinha.pt',
        '2025-04-30 14:30:20',
        '2025-04-30 14:30:20'
    ),
    (
        '1463869053',
        'DIRECÇÃO DE  ABASTECIMENTO',
        'SCH FZ Lopes Pereira',
        'alberto.lopes.pereira@marinha.pt',
        '2025-04-30 14:34:30',
        '2025-04-30 14:34:30'
    ),
    (
        '1456570791',
        'DIRECÇÃO GERAL DA AUTORIDADE MARÍTIMA',
        'CAB CM Manjolinho Costa',
        'dgam_dti05@marinha.pt',
        '2025-04-30 14:35:43',
        '2025-04-30 14:35:43'
    ),
    (
        '1445769058',
        'CENTRO DE EXPERIMENTAÇÃO OPERACIONAL DA MARINHA',
        'CTEN ST-EELT Castro Veloso',
        'castro.veloso@marinha.pt',
        '2025-04-30 14:36:49',
        '2025-04-30 14:36:49'
    ),
    (
        '1423869054',
        'INSTITUTO HIDROGRÁFICO',
        'CTEN ST-EINF Deolinda Marisa Pedrosa',
        'dd.das.chf@hidrografico.pt',
        '2025-04-30 14:37:35',
        '2025-04-30 14:37:35'
    ),
    (
        '1468369621',
        'DIRECÇÃO DE PESSOAL',
        'CTEN STP Bastos Monsanto',
        'dp.danc.scsi.chefe@marinha.pt',
        '2025-04-30 14:38:28',
        '2025-04-30 14:38:28'
    ),
    (
        '1428269182',
        'NRP ÁLVARES  CABRAL',
        '1SAR C Barata Gonçalves',
        'nrpacabral.3221@marinha.pt',
        '2025-04-30 14:40:23',
        '2025-04-30 14:40:23'
    ),
    (
        '1467269170',
        'NRP  AURIGA',
        'CFR EN-MEC Oliveira Azenha',
        'oliveira.azenha@marinha.pt',
        '2025-04-30 14:42:56',
        '2025-04-30 14:42:56'
    ),
    (
        '1467269176',
        'DEPOSITO MUNIÇÕES  NATO LX',
        '2SAR ETI Silva Ferreira',
        'dmnl.sag.ele.infor@marinha.pt',
        '2025-04-30 14:44:03',
        '2025-04-30 14:44:03'
    ),
    (
        '1460770685',
        'ESQUADRILHA DE NAVIOS DE SUPERFÍCIE',
        '1SAR ETI Vedor Carolino',
        'vedor.carolino@marinha.pt',
        '2025-04-30 14:44:44',
        '2025-04-30 14:44:44'
    ),
    (
        '1465869531',
        'COMANDO DA ZONA MARITIMA DOS AÇORES',
        'SAJ ETC Andreia Vieira de Jesus',
        'czma.dap.sel.cssc@marinha.pt',
        '2025-04-30 14:46:00',
        '2025-04-30 14:46:00'
    ),
    (
        '1450369177',
        'DEPÓSITO POLNATO DE PONTA DELGADA',
        'SAJ ETC Andreia Vieira de Jesus',
        'czma.dap.sel.cssc@marinha.pt',
        '2025-04-30 14:46:25',
        '2025-04-30 14:46:25'
    ),
    (
        '1445769051',
        'DIRECÇÃO JURÍDICA',
        'SAJ A Teixeira Botelho',
        'dj.chefesecretaria@marinha.pt',
        '2025-04-30 14:47:09',
        '2025-04-30 14:47:09'
    ),
    (
        '1454869052',
        'INSPECÇÃO GERAL DA MARINHA',
        'SAJ L Vera Fonte',
        'vera.lucia.fonte@marinha.pt',
        '2025-04-30 14:48:01',
        '2025-04-30 14:48:01'
    ),
    (
        '1461369171',
        'NRP  CASSIOPEIA',
        'CAB C Alves Fernandes',
        'alves.fernandes@marinha.pt',
        '2025-04-30 14:48:59',
        '2025-04-30 14:48:59'
    ),
    (
        '1423369172',
        'CENTRO DE COMUNICAÇÕES DE DADOS E CIFRA DA MARINHA',
        'SAJ C Santos Favinha',
        'ccdcm.ssic.ssi.ch@marinha.pt',
        '2025-04-30 14:51:18',
        '2025-04-30 14:51:18'
    ),
    (
        '1434869057',
        'DIRECÇÃO DE INFRA ESTRUTURAS',
        'SCH FZ Henriques Pereira',
        'henriques.pereira@marinha.pt',
        '2025-04-30 14:53:49',
        '2025-04-30 14:53:49'
    ),
    (
        '1400070682',
        'ESTADO MAIOR DA ARMADA',
        '1SAR FZ Amaral Gomes',
        'ema_adu@marinha.pt',
        '2025-04-30 14:54:45',
        '2025-04-30 14:54:45'
    ),
    (
        '1404869059',
        'CENTRO MEDICINA  NAVAL',
        '1SAR FZ Magalhães Pinto',
        'cmn_adu@marinha.pt',
        '2025-04-30 14:55:53',
        '2025-04-30 14:55:53'
    );

INSERT INTO
    users (
        username,
        display_name,
        email,
        is_admin,
        last_login
    )
VALUES (
        'm24685',
        'COM Dias Correia',
        'dias.correia@marinha.pt',
        1,
        '2025-07-01 22:45:55'
    ),
    (
        'm915489',
        'CTEN TSN-GES Pires Silveiro',
        'pires.silveiro@marinha.pt',
        1,
        '2025-08-08 15:23:49'
    ),
    (
        'm9336502',
        'CAB L Francisco Moreno',
        'francisco.moreno@marinha.pt',
        0,
        '2025-09-16 14:47:59'
    ),
    (
        'm9102205',
        'CTEN TSN-ELT Olívia Maria Boieiro',
        'olivia.maria.boieiro@marinha.pt',
        0,
        '2025-04-01 10:39:13'
    ),
    (
        'm9822905',
        'STEN STP Caetano Mendes',
        'caetano.mendes@marinha.pt',
        1,
        '2025-09-16 14:57:35'
    ),
    (
        'm9300400',
        '1SAR L Cláudia Romba',
        'claudia.alexandra.romba@marinha.pt',
        0,
        NULL
    ),
    (
        'm9338502',
        'CAB L Melo Caetano',
        'melo.caetano@marinha.pt',
        0,
        '2025-04-23 10:35:47'
    ),
    (
        'm9301210',
        '1SAR L Vendeira',
        'marina.andreia.vendeira@marinha.pt',
        0,
        '2025-04-01 12:42:13'
    ),
    (
        'm9347094',
        'SAJ C Sandra Oliveira',
        'lourenco.oliveira@marinha.pt',
        1,
        '2025-05-28 08:48:25'
    ),
    (
        'm903290',
        '1SAR C Silverinha Roxo',
        'silveirinha.roxo@marinha.pt',
        1,
        '2025-07-16 08:12:29'
    ),
    (
        'm850488',
        'CFR Pinto Alves',
        'pinto.alves@marinha.pt',
        0,
        '2025-07-09 14:29:01'
    ),
    (
        'm22600',
        'CFR EN-AEL Pacheco Raimundo',
        'pacheco.raimundo@marinha.pt',
        1,
        '2025-07-01 22:45:55'
    );
