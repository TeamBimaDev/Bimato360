INSERT INTO public.core_bimacorenotificationtype (id, public_id, created, updated, name, active, code, is_system)
VALUES (1, 'a23ca411-f537-4dd5-9049-edb161778e8c', '2023-09-14 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Notification payment retard', true, 'NOTIFICATION_PAYMENT_LATE', true),
       (2, '6360650e-79cd-4eb8-8ff8-239c25714c13', '2023-09-14 13:10:58.365633+01', '2023-08-22 13:10:58.365633+01',
        'Notification rappel de payment', true, 'NOTIFICATION_PAYMENT_REMINDER', true);



ALTER SEQUENCE public.core_bimacorenotificationtype_id_seq RESTART WITH 3;
SELECT pg_catalog.setval('public.core_bimacorenotificationtype_id_seq', 3, true);



INSERT INTO public.core_bimacorenotificationtemplate (id, public_id, created, updated, name, company_id, subject,
                                                      message, notification_type_id)
VALUES (1, 'cf6fdd6a-2674-4d3b-861d-5f65fba1dc5c', '2023-09-14 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Notification payment retard', 1, 'Rappel de Retard de Paiement - Facture {{invoice_number}}',
        'Cher {{partner_name}},<br/><br/>Malheureusement, nous constatons qu''à ce jour, la facture avec la référence {{invoice_number}} n''a pas été réglée, bien que la date d''échéance soit passée. <br/>Veuillez trouver Ci-joint la communication de votre facture impayée.<br/>{{due_date}}<br/>Montant TTC : {{total_amount}}<br/>Montant payée : {{total_amount_paid}}<br/>Montant restant : {{amount_remaining}}<br/>Nous vous encourageons à effectuer le paiement dès que possible pour éviter tout retard supplémentaire.<br/><br/>Cordialement,<br/>{{company_name}}',
        1);

ALTER SEQUENCE public.core_bimacorenotificationtemplate_id_seq RESTART WITH 2;
SELECT pg_catalog.setval('public.core_bimacorenotificationtemplate_id_seq', 2, true);

INSERT INTO public.core_bimacorenotificationtemplate (id, public_id, created, updated, name, company_id, subject,
                                                      message, notification_type_id)
VALUES (2, 'ead43f11-9509-42aa-b7d9-01fb9b443853', '2023-09-14 13:10:43.065253+01', '2023-08-22 13:10:43.065253+01',
        'Notification rappel de paiment', 1, 'Rappel de Paiement - Facture {{invoice_number}}',
        'Cher {{partner_name}},<br/><br/>Ceci un rappel pour le paiment de la facture avec la référence {{invoice_number}}<br/>, <br/>Veuillez trouver Ci-joint la communication de votre facture impayée.<br/>{{due_date}}<br/>Montant TTC : {{total_amount}}<br/>Montant payée : {{total_amount_paid}}<br/>Montant restant : {{amount_remaining}}<br/>Nous vous encourageons à effectuer le paiement dès que possible pour éviter tout retard supplémentaire.<br/><br/>Cordialement,<br/>{{company_name}}',
        2);

ALTER SEQUENCE public.core_bimacorenotificationtemplate_id_seq RESTART WITH 3;
SELECT pg_catalog.setval('public.core_bimacorenotificationtemplate_id_seq', 3, true);
