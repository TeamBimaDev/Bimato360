INSERT INTO public.treasury_bimatreasurytransactiontype (id, public_id, created, updated, name, active, code, is_system,
                                                         income_outcome, cash_bank)
VALUES (1, 'b76eab54-8a85-40fc-971b-9c09756837bb', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Caisse Vers Compte', true, 'FROM_CASH_TO_ACCOUNT_INCOME', true, 'INCOME', 'BANK'),
       (2, '4c6fe1a0-d4fc-4c02-ab30-70b53bc18758', '2023-08-22 13:10:58.365633+01', '2023-08-22 13:10:58.365633+01',
        'Compte Vers Caisse', true, 'FROM_ACCOUNT_TO_CASH_INCOME', true, 'INCOME', 'CASH'),
       (3, 'e4c288a2-8cf7-45e8-9f60-0caa5855f490', '2023-08-22 13:11:11.919061+01', '2023-08-22 13:11:11.919061+01',
        'Caisse Vers Compte', true, 'FROM_CASH_TO_ACCOUNT_OUTCOME', true, 'OUTCOME', 'CASH'),
       (4, '94f63440-bfb6-484c-8146-4dabad3f4554', '2023-08-22 13:11:27.372995+01', '2023-08-22 13:11:27.372995+01',
        'Compte Vers Caisse', true, 'FROM_ACCOUNT_TO_CASH_OUTCOME', true, 'OUTCOME', 'BANK'),
       (5, '44c60e44-2dd3-4ab9-a0c8-73df19373805', '2023-08-22 13:11:40.38992+01', '2023-08-22 13:11:40.38992+01',
        'Solde Initial', true, 'INITIAL_BALANCE_ACCOUNT', true, 'INCOME', 'BANK'),
       (6, '9bcfab43-7c4c-4226-96e9-19920d4e4644', '2023-08-22 13:11:48.773962+01', '2023-08-22 13:11:48.773962+01',
        'Solde Initial', true, 'INITIAL_BALANCE_CASH', true, 'INCOME', 'CASH'),
       (7, '4842a12d-4031-4e73-8027-9215ff3f85ac', '2023-08-22 13:12:01.510077+01', '2023-08-22 13:12:01.510077+01',
        'Versement Entrée', true, 'TRANSFER_INCOME', true, 'INCOME', 'BANK'),
       (8, 'b2842222-9773-4bce-b8a3-9cc7d94eafad', '2023-08-22 13:12:08.014837+01', '2023-08-22 13:12:08.014837+01',
        'Versement Sortie', true, 'TRANSFER_OUTCOME', true, 'OUTCOME', 'BANK'),
       (9, '57289fb5-fa33-4857-9585-9f0047d0b064', '2023-08-22 13:12:16.422225+01', '2023-08-22 13:12:16.422225+01',
        'Chèque Entrée', true, 'CHECK_INCOME', true, 'INCOME', 'BANK'),
       (10, '8b3eb265-c2b6-4c76-90bc-296b10913dad', '2023-08-22 13:12:24.213963+01', '2023-08-22 13:12:24.213963+01',
        'Chèque Sortie', true, 'CHECK_OUTCOME', true, 'OUTCOME', 'BANK'),
       (11, '52664e8b-8d9c-49e6-b527-a66365a93463', '2023-08-22 13:12:33.010475+01', '2023-08-22 13:12:33.010475+01',
        'Salaire', true, 'SALARY_OUTCOME', true, 'OUTCOME', 'BANK'),
       (12, '52664e8b-8d9c-49e6-b527-a66365a93556', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Payment Facture Client', true, 'INVOICE_PAYMENT_BANK', true, 'INCOME', 'BANK'),
       (13, '325cb624-1f1e-42a5-8945-b7b287548b1d', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Payment Facture Client', true, 'INVOICE_PAYMENT_CASH', true, 'INCOME', 'CASH'),
       (14, '125d3e0e-1674-479d-8b17-b4a364e73a03', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Règelemnt Facture Fournisseur', true, 'INVOICE_PAYMENT_OUTCOME_BANK', true, 'OUTCOME', 'BANK'),
       (15, 'f2af0cde-bd8e-4fbc-820f-b6582735e050', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Règelemnt Facture Fournisseur', true, 'INVOICE_PAYMENT_OUTCOME_CASH', true, 'OUTCOME', 'CASH');

ALTER SEQUENCE public.treasury_bimatreasurytransactiontype_id_seq RESTART WITH 16;
SELECT pg_catalog.setval('public.treasury_bimatreasurytransactiontype_id_seq', 16, true);

delete from public.treasury_bimatreasurytransaction where transaction_type_id in  in (5, 6, 7, 8, 9, 10, 11);

delete from public.treasury_bimatreasurytransactiontype where id in (5, 6, 7, 8, 9, 10, 11);

INSERT INTO public.treasury_bimatreasurytransactiontype (id, public_id, created, updated, name, active, code, is_system,
                                                         income_outcome, cash_bank)
VALUES (16, '7e418c5e-d33e-4fd1-8012-9b110f95c416', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Depôt de fond', true, 'DEPOT_FOND_INCOME_BANK', true, 'INCOME', 'BANK'),
       (17, 'a2a9ef26-e60b-4517-aaea-28e12d8bd68e', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Depôt de fond', true, 'DEPOT_FOND_INCOME_CASH', true, 'INCOME', 'CASH'),
       (18, '57335998-d669-4f55-9418-f634986b8947', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Charge Entreprise', true, 'CHARGE_ENTREPRISE_OUTCOME_BANK', true, 'OUTCOME', 'BANK'),
       (19, '10203f49-d7c9-4ba0-8b58-bb1924ed4929', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Charge Entreprise', true, 'CHARGE_ENTREPRISE_OUTCOME_CASH', true, 'OUTCOME', 'CASH');

ALTER SEQUENCE public.treasury_bimatreasurytransactiontype_id_seq RESTART WITH 20;
SELECT pg_catalog.setval('public.treasury_bimatreasurytransactiontype_id_seq', 20, true);