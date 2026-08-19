CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,

    user_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ideas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- N:1 relationship: each idea belongs to one user
    user_id INT NOT NULL,

    title VARCHAR(150) NOT NULL,
    description TEXT,

    status ENUM (
        'DRAFT',
        'PENDING',
        'ANALYZING',
        'DONE',
        'ARCHIVED'
    ) DEFAULT 'DRAFT',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
);

CREATE TABLE idea_5w2h (
    id INT PRIMARY KEY AUTO_INCREMENT,

    -- 1:1 relationship: each idea has one current 5W2H
    idea_id INT NOT NULL UNIQUE,

    what TEXT,
    what_source ENUM('USER', 'AI', 'USER_EDITED_AI'),

    why TEXT,
    why_source ENUM('USER', 'AI', 'USER_EDITED_AI'),

    who TEXT,
    who_source ENUM('USER', 'AI', 'USER_EDITED_AI'),

    where_location TEXT,
    where_location_source ENUM('USER', 'AI', 'USER_EDITED_AI'),

    when_info TEXT,
    when_source ENUM('USER', 'AI', 'USER_EDITED_AI'),

    how TEXT,
    how_source ENUM('USER', 'AI', 'USER_EDITED_AI'),

    how_much TEXT,
    how_much_source ENUM('USER', 'AI', 'USER_EDITED_AI'),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (idea_id)
        REFERENCES ideas(id)
        ON DELETE CASCADE
);

CREATE TABLE ai_analysis (
    id INT PRIMARY KEY AUTO_INCREMENT,

    -- N:1 relationship: an idea can have multiple AI analyses
    idea_id INT NOT NULL,

    score INT,
    analysis_data JSON,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (idea_id)
        REFERENCES ideas(id)
        ON DELETE CASCADE
)