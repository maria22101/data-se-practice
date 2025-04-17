/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
SELECT
    c.name AS category_name,
    COUNT(f.film_id) AS film_count
FROM film f
         JOIN film_category fc ON f.film_id = fc.film_id
         JOIN category c ON c.category_id = fc.category_id
GROUP BY c.name
ORDER BY film_count DESC;



/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
SELECT
    a.first_name,
    a.last_name,
    ranked_actors.rental_count
FROM (SELECT
          fa.actor_id,
          COUNT(r.rental_id) AS rental_count,
          ROW_NUMBER() OVER (ORDER BY COUNT(r.rental_id) DESC) AS rn
      FROM rental r
               JOIN inventory i ON r.inventory_id = i.inventory_id
               JOIN film_actor fa ON i.film_id = fa.film_id
      GROUP BY fa.actor_id) AS ranked_actors
JOIN actor a ON a.actor_id = ranked_actors.actor_id
WHERE ranked_actors.rn <= 10
ORDER BY rental_count DESC;



/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
-- SQL code goes here...
WITH category_earnings AS
         (SELECT
              fc.category_id,
              SUM(p.amount) AS earnings
          FROM inventory i
                   JOIN film_category fc ON i.film_id = fc.film_id
                   JOIN rental r ON i.inventory_id = r.inventory_id
                   JOIN payment p ON r.rental_id = p.rental_id
          GROUP BY fc.category_id)
SELECT
    c.name
FROM category_earnings
         JOIN category c ON c.category_id = category_earnings.category_id
ORDER BY earnings DESC
LIMIT 1;

-- або
SELECT
    c.name
FROM (SELECT
          fc.category_id,
          RANK() OVER (ORDER BY SUM(p.amount) DESC) AS earnings_rank
      FROM inventory i
               JOIN film_category fc ON i.film_id = fc.film_id
               JOIN rental r ON i.inventory_id = r.inventory_id
               JOIN payment p ON r.rental_id = p.rental_id
      GROUP BY fc.category_id) AS categories_ranked_by_earnings
JOIN category c ON c.category_id = categories_ranked_by_earnings.category_id
WHERE earnings_rank = 1;



/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
SELECT
    f.title
FROM film f
WHERE NOT EXISTS(SELECT 1
                 FROM inventory i
                 WHERE i.film_id = f.film_id);
-- або
SELECT
    f.title
FROM film f
         LEFT JOIN inventory i ON f.film_id = i.film_id
WHERE i.film_id IS NULL;



/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
WITH top_three_actors AS
         (SELECT
              fa.actor_id,
              COUNT(actor_id) AS actor_count
          FROM film_actor fa
                   JOIN film_category fc ON fa.film_id = fc.film_id
                   JOIN category c ON c.category_id = fc.category_id
          WHERE c.name = 'Children'
          GROUP BY fa.actor_id
          ORDER BY actor_count DESC
          LIMIT 3)
SELECT
    a.first_name,
    a.last_name
FROM top_three_actors tta
         JOIN actor a ON a.actor_id = tta.actor_id;