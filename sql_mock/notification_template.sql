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



INSERT INTO public.core_bimacorenotificationtype (id, public_id, created, updated, name, active, code, is_system)
VALUES (3, '2122f611-0cb8-43f3-a25c-6e0e96111e2c', '2023-10-11 13:10:43.065253+01', '2023-10-11 13:10:43.065253+01',
        'Notification de demande de congé', true, 'NOTIFICATION_VACATION_REQUEST', true);

ALTER SEQUENCE public.core_bimacorenotificationtype_id_seq RESTART WITH 4;
SELECT pg_catalog.setval('public.core_bimacorenotificationtype_id_seq', 4, true);



INSERT INTO public.core_bimacorenotificationtemplate (id, public_id, created, updated, name, company_id, subject,
                                                      message, notification_type_id)
VALUES (3, '12c77a2c-2523-4622-b2ac-efc2b2dfc211', '2023-10-11 13:10:43.065253+01', '2023-10-11 13:10:43.065253+01',
        'Notification de demande de congé', 1, 'Notification de demande de congé {{employee_full_name}}',
        'Cher {{manager_full_name}},<br/><br/> Une nouvelle demande de congé a été déposer par Mr {{employee_full_name}} pour la periode du {{vacation_date_start}} au {{vacation_date_end}} pour la rasion suivant : <br/> {{vacation_reason}} <br/><br/> Merci de connecter sur votre espace pour gérer ce demande.',
        3);

ALTER SEQUENCE public.core_bimacorenotificationtemplate_id_seq RESTART WITH 4;
SELECT pg_catalog.setval('public.core_bimacorenotificationtemplate_id_seq', 4, true);



INSERT INTO public.core_bimacorenotificationtype (id, public_id, created, updated, name, active, code, is_system)
VALUES (5, 'bc3b4823-0a24-4ab7-a44a-0c8c0e50ff9a', '2023-10-11 13:10:43.065253+01', '2023-10-11 13:10:43.065253+01',
        'Notification: Congé approuver', true, 'NOTIFICATION_VACATION_APPROVAL', true),
       (6, '806a764c-d50b-4dbd-b5b5-ed69f98b4d01', '2023-10-11 13:10:43.065253+01', '2023-10-11 13:10:43.065253+01',
        'Notification: Congé réfuser', true, 'NOTIFICATION_VACATION_REFUSAL', true);

ALTER SEQUENCE public.core_bimacorenotificationtype_id_seq RESTART WITH 7;
SELECT pg_catalog.setval('public.core_bimacorenotificationtype_id_seq', 7, true);


INSERT INTO public.core_bimacorenotificationtemplate (id, public_id, created, updated, name, company_id, subject,
                                                      message, notification_type_id)
VALUES (5, 'e116e286-50dd-4e9d-8e9b-164be71cda49', '2023-10-11 13:10:43.065253+01', '2023-10-11 13:10:43.065253+01',
        'Notification : congé approuver', 1, 'Vacation Approval for {{employee_full_name}}',
        'Dear {{employee_full_name}},<br/>We are happy to inform you that your vacation request for the period from {{vacation_date_start}} to {{vacation_date_end}} has been approved. Enjoy your time off!<br/><br/>Best regards,Your HR Team.',
        5),
       (6, 'fd832803-3254-48ef-93d0-4d62ee9b2b53', '2023-10-11 13:10:43.065253+01', '2023-10-11 13:10:43.065253+01',
        'Notification : congé réfuser', 1, 'Vacation Refusal for {{employee_full_name}}',
        'Dear {{employee_full_name}},<br/>Unfortunately, your vacation request for the period from {{vacation_date_start}} to {{vacation_date_end}} has been disapproved for the following reason: {{reason_refused}}. Please feel free to discuss this decision with your manager or HR representative.<br/><br/>Best regards,Your HR Team.',
        6);

ALTER SEQUENCE public.core_bimacorenotificationtemplate_id_seq RESTART WITH 7;
SELECT pg_catalog.setval('public.core_bimacorenotificationtemplate_id_seq', 7, true);



INSERT INTO public.core_bimacorenotificationtype (id, public_id, created, updated, name, active, code, is_system)
VALUES (8, '3a3f7620-92e0-4525-9c73-460317808e4b', '2023-10-11 13:10:43.065253+01', '2023-10-11 13:10:43.065253+01',
        'Nofitication : Contract renew', true, 'NOTIFICATION_CONTRACT_EXPIRY_SOON', true);

ALTER SEQUENCE public.core_bimacorenotificationtype_id_seq RESTART WITH 9;
SELECT pg_catalog.setval('public.core_bimacorenotificationtype_id_seq', 9, true);

INSERT INTO public.core_bimacorenotificationtemplate (id, public_id, created, updated, name, company_id, subject,
                                                      message, notification_type_id)
VALUES (8, '453cd1a4-962c-4905-b685-b63371e75da4', '2023-10-11 13:10:43.065253+01', '2023-10-11 13:10:43.065253+01',
        'Notification : contract renew', 1,
        'Contract Alert: {{employee_full_name}}''s contract ends in {{remaining_days}} days',
        'Dear Team,<br/>This is a reminder that the contract of {{employee_full_name}} in the {{department_name}} department is set to end in {{remaining_days}} days on {{contract_end_date}}. <br/><br/>Please take the necessary steps to review and address this matter.<br/><br/>Best regards,<br/>Your HR Team',
        8);

ALTER SEQUENCE public.core_bimacorenotificationtemplate_id_seq RESTART WITH 9;
SELECT pg_catalog.setval('public.core_bimacorenotificationtemplate_id_seq', 9, true);


INSERT INTO public.core_bimacorenotificationtype (id, public_id, created, updated, name, active, code, is_system)
VALUES (9, '764bc066-db10-45ea-b69d-711e319e1fe7', '2023-10-13 13:10:43.065253+01', '2023-10-13 13:10:43.065253+01',
        'Nofitication : Invitation to an activity', true, 'NOTIFICATION_ACTIVITY_INVITATION', true);

ALTER SEQUENCE public.core_bimacorenotificationtype_id_seq RESTART WITH 10;
SELECT pg_catalog.setval('public.core_bimacorenotificationtype_id_seq', 10, true);


INSERT INTO public.core_bimacorenotificationtemplate (id, public_id, created, updated, name, company_id, subject,
                                                      message, notification_type_id)
VALUES (9, 'a785ab8b-90c5-43be-b7ec-94b1adfb2692', '2023-10-11 13:10:43.065253+01', '2023-10-11 13:10:43.065253+01',
        'Notification : Invitation to an activity', 1,
        'Invitation: Participation in {{activity_name}} from {{activity_start_date}} to {{activity_end_date}}',
        'Dear {{person_full_name}},<br/><br/>We are pleased to invite you to participate in the activity titled "{{activity_name}}", which is scheduled to take place from {{activity_start_date}} to {{activity_end_date}}.<br/><br/>Here is a brief description of the activity:<br/>{activity_description}}<br/>Your involvement and contributions to the success of this activity are highly valued. We believe that your participation will add significant value and we look forward to your positive confirmation.<br/><br/>To confirm your participation, please log in to your account.<br/><br/>Should you have any questions or require further information, feel free to contact us at any time.<br/><br/>Thank you for your attention and cooperation.<br/><br/>Warmest regards',
        9);

ALTER SEQUENCE public.core_bimacorenotificationtemplate_id_seq RESTART WITH 10;
SELECT pg_catalog.setval('public.core_bimacorenotificationtemplate_id_seq', 10, true);