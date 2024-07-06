INSERT INTO public.treasury_bimatreasurypaymentmethod (id, public_id, created, updated, name, active, code, is_system,
                                                       income_outcome, cash_bank)
VALUES (1, 'd467db1b-b845-428f-aace-6ffaab90412f', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Espèce Entrée', true, 'CASH_PAYMENT_INCOME', true, 'INCOME', 'CASH'),
       (2, '77984bbe-23b7-4ddc-bf52-0020b25f2174', '2023-08-22 13:10:58.365633+01', '2023-08-22 13:10:58.365633+01',
        'Espèce Sortie', true, 'CASH_PAYMENT_OUTCOME', true, 'OUTCOME', 'CASH'),
       (3, '02acf660-6980-4ddc-9a2c-fde28f46df12', '2023-08-22 13:12:01.510077+01', '2023-08-22 13:12:01.510077+01',
        'Versement Entrée', true, 'TRANSFER_INCOME', true, 'INCOME', 'BANK'),
       (4, 'b83837f0-0266-4350-a07b-c9e325274790', '2023-08-22 13:12:08.014837+01', '2023-08-22 13:12:08.014837+01',
        'Versement Sortie', true, 'TRANSFER_OUTCOME', true, 'OUTCOME', 'BANK'),
       (5, '37f0c3ae-089a-446c-bd92-cd4a556a4f58', '2023-08-22 13:12:16.422225+01', '2023-08-22 13:12:16.422225+01',
        'Chèque Entrée', true, 'CHECK_INCOME', true, 'INCOME', 'BANK'),
       (6, '87e8a20f-708e-4ee5-b151-0913c0f33f98', '2023-08-22 13:12:24.213963+01', '2023-08-22 13:12:24.213963+01',
        'Chèque Sortie', true, 'CHECK_OUTCOME', true, 'OUTCOME', 'BANK'),
       (7, 'f6a10701-8083-41a7-a738-e63cfc12b607', '2023-08-22 13:12:33.010475+01', '2023-08-22 13:12:33.010475+01',
        'Carte Bancaire', true, 'CREDIT_CARD_INCOME', true, 'INCOME', 'BANK'),
       (8, 'b6de2875-6d8a-4701-94d2-9817cda33117', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Carte Bancaire', true, 'CREDIT_CARD_OUTCOME', true, 'OUTCOME', 'BANK'),
       (9, '899db017-d0cd-4b78-990b-11ca7c0a415d', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Virement Entrée', true, 'VIRMENT_INCOME', true, 'INCOME', 'BANK'),
       (10, '10002619-a9d2-4dff-9e0a-2c6af87c50b0', '2023-08-22 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Virement Sortie', true, 'VIRMENT_OUTCOME', true, 'OUTCOME', 'BANK');


ALTER SEQUENCE public.treasury_bimatreasurypaymentmethod_id_seq RESTART WITH 11;
SELECT pg_catalog.setval('public.treasury_bimatreasurypaymentmethod_id_seq', 11, true);