--> Table Creation 
CREATE TABLE internships (

    id SERIAL PRIMARY KEY,
	
    role_category TEXT,
    internship_title TEXT,
    company TEXT,
    internship_link TEXT,
    location TEXT,
	stipend TEXT,
	posting_date TEXT,
	min_stipend NUMERIC,
    max_stipend NUMERIC,
    avg_stipend NUMERIC,

    stipend_type TEXT,

    
    posting_days_ago NUMERIC,
    city TEXT,
    work_mode TEXT

);

select * 
from internships
limit 10;

SELECT COUNT(*)
FROM internships;



--> QUERY 1 — Highest Paying Internship Categories

SELECT
    role_category,

    ROUND(
        AVG(avg_stipend),
        2
    ) AS average_stipend,

    COUNT(*) AS total_openings

FROM internships

WHERE avg_stipend IS NOT NULL

GROUP BY role_category

ORDER BY average_stipend DESC;


--> QUERY 2 — 2. Which Cities Have the Most Internship Opportunities?

SELECT
    city,
    COUNT(*) AS total_internships

FROM internships

WHERE city IS NOT NULL

GROUP BY city

ORDER BY total_internships DESC

LIMIT 10;


--> QUERY 3 - Which Work Mode Offers the Highest Average Stipend?

SELECT
    work_mode,

    COUNT(*) AS total_roles,

    ROUND(
        AVG(avg_stipend),
        2
    ) AS average_salary

FROM internships

WHERE avg_stipend IS NOT NULL

GROUP BY work_mode

ORDER BY average_salary DESC;


--> QUERY 4  - Which Companies Hire Most Frequently?

SELECT
    company,
    COUNT(*) AS total_openings

FROM internships

GROUP BY company

ORDER BY total_openings DESC

LIMIT 10;


--> QUERY 5 - Which Companies Offer the Highest Average Stipend?

SELECT
    company,

    ROUND(
        AVG(avg_stipend),
        2
    ) AS average_salary,

    COUNT(*) AS openings

FROM internships

WHERE avg_stipend IS NOT NULL

GROUP BY company

HAVING COUNT(*) >= 2

ORDER BY average_salary DESC

LIMIT 10;


--> QUERY 6 - What Percentage of Internships Are Paid vs Unpaid?

SELECT
    stipend_type,

    COUNT(*) AS total_roles,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER(),
        2
    ) AS percentage

FROM internships

GROUP BY stipend_type

ORDER BY percentage DESC;


--> QUERY 7 - Which Internship Titles Have the Highest Salaries?

SELECT
    internship_title,
    company,
    avg_stipend,

    RANK() OVER(
        ORDER BY avg_stipend DESC
    ) AS salary_rank

FROM internships

WHERE avg_stipend IS NOT NULL

LIMIT 15;


--> QUERY 8 - Which Internship Categories Have the Most Openings?

SELECT
    role_category,
    COUNT(*) AS total_openings

FROM internships

GROUP BY role_category

ORDER BY total_openings DESC;


--> QUERY 9 - What Is the Salary Distribution Across Internships?

SELECT

    CASE

        WHEN avg_stipend < 5000
            THEN 'Low Paying'

        WHEN avg_stipend BETWEEN 5000 AND 15000
            THEN 'Medium Paying'

        WHEN avg_stipend > 15000
            THEN 'High Paying'

        ELSE 'Unknown'

    END AS salary_category,

    COUNT(*) AS total_roles

FROM internships

WHERE avg_stipend IS NOT NULL

GROUP BY salary_category;


--> QUERY 10 - Which Cities Offer the Highest Average Stipend?

SELECT
    city,

    ROUND(
        AVG(avg_stipend),
        2
    ) AS average_salary,

    COUNT(*) AS openings

FROM internships

WHERE
    avg_stipend IS NOT NULL
    AND city IS NOT NULL

GROUP BY city

HAVING COUNT(*) >= 3

ORDER BY average_salary DESC

LIMIT 10;


