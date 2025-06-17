# Defenses

## Decision-based Adversarial Attack
- Ограничить частоту запросов (rate-limiting, CAPTCHA)  
- Фильтровать входные вектора по статистике train (input validation, clip_bounds)  
- Внедрить adversarial training или randomized smoothing для табличных моделей  
- Мониторить аномалии запросов (SIEM-сигналы при всплесках ошибок или необычных паттернах)  
- Использовать ансамбли моделей и случайные преобразования входа (feature randomization)

## Model Extraction Attack
- Ввести throttling и квоты на API-запросы  
- Спрятать или округлить вероятности (output perturbation, differential privacy)  
- Внедрить модель-водяной знак (watermarking) и fingerprinting для отслеживания утечек  
- Настроить строгую аутентификацию и авторизацию для всех endpoint  
- Анализировать паттерны запросов (детектировать ботов и автоматический скрейпинг)

## Membership Inference Attack
- Не возвращать сырые confidence-оценки, а выдавать только топ-класс или защищённые метки  
- Применить prediction clipping и добавить случайный шум в вероятности (output noise)  
- Обучать модель с differential privacy (DP-SGD)  
- Группировать запросы в пачки (batch-prediction) для снижения детализации отклика  
- Ограничить общий объём inference-запросов для одного клиента  

---

Будет хороший базовый уровень защиты ML-моделей скоринга. Их стоит интегрировать их в CI/CD pipeline и audit-логи, чтобы атаки сразу попадали в зону ответственности ИБ
