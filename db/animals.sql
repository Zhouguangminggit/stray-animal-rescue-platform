CREATE TABLE IF NOT EXISTS animals_animalcategory (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  sort_order INT UNSIGNED NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS animals_animal (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  category_id BIGINT NOT NULL,
  name VARCHAR(80) NOT NULL DEFAULT '',
  gender VARCHAR(10) NOT NULL DEFAULT 'unknown',
  estimated_age VARCHAR(50) NOT NULL DEFAULT '',
  health_status VARCHAR(20) NOT NULL DEFAULT 'unknown',
  rescue_status VARCHAR(20) NOT NULL DEFAULT 'waiting',
  adoption_status VARCHAR(20) NOT NULL DEFAULT 'unavailable',
  campus_id BIGINT NOT NULL,
  found_location VARCHAR(255) NOT NULL,
  description LONGTEXT NOT NULL,
  is_published BOOLEAN NOT NULL DEFAULT TRUE,
  published_at DATETIME(6) NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  INDEX animal_rescue_pub_idx (is_published, rescue_status, published_at DESC),
  INDEX animal_filter_idx (category_id, health_status, campus_id),
  CONSTRAINT animal_category_fk FOREIGN KEY (category_id) REFERENCES animals_animalcategory(id),
  CONSTRAINT animal_campus_fk FOREIGN KEY (campus_id) REFERENCES campuses_campus(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS animals_animal_tags (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  animal_id BIGINT NOT NULL,
  tag_id BIGINT NOT NULL,
  UNIQUE KEY animals_animal_tag_unique (animal_id, tag_id),
  CONSTRAINT animal_tags_animal_fk FOREIGN KEY (animal_id) REFERENCES animals_animal(id),
  CONSTRAINT animal_tags_tag_fk FOREIGN KEY (tag_id) REFERENCES tags_tag(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS animals_animalimage (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  animal_id BIGINT NOT NULL,
  image VARCHAR(100) NOT NULL,
  caption VARCHAR(100) NOT NULL DEFAULT '',
  is_cover BOOLEAN NOT NULL DEFAULT FALSE,
  sort_order INT UNSIGNED NOT NULL DEFAULT 0,
  INDEX animal_image_animal_idx (animal_id),
  CONSTRAINT animal_image_animal_fk FOREIGN KEY (animal_id) REFERENCES animals_animal(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS animals_rescuerequest (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  applicant_id BIGINT NOT NULL,
  category_id BIGINT NOT NULL,
  animal_name VARCHAR(80) NOT NULL DEFAULT '',
  gender VARCHAR(10) NOT NULL DEFAULT 'unknown',
  health_status VARCHAR(20) NOT NULL DEFAULT 'unknown',
  campus_id BIGINT NOT NULL,
  found_location VARCHAR(255) NOT NULL,
  description LONGTEXT NOT NULL,
  contact VARCHAR(100) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  review_note LONGTEXT NOT NULL,
  reviewed_by_id BIGINT NULL,
  reviewed_at DATETIME(6) NULL,
  approved_animal_id BIGINT NULL UNIQUE,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  INDEX rescue_review_idx (status, created_at DESC),
  CONSTRAINT rescue_applicant_fk FOREIGN KEY (applicant_id) REFERENCES accounts_user(id),
  CONSTRAINT rescue_reviewer_fk FOREIGN KEY (reviewed_by_id) REFERENCES accounts_user(id),
  CONSTRAINT rescue_category_fk FOREIGN KEY (category_id) REFERENCES animals_animalcategory(id),
  CONSTRAINT rescue_campus_fk FOREIGN KEY (campus_id) REFERENCES campuses_campus(id),
  CONSTRAINT rescue_approved_animal_fk FOREIGN KEY (approved_animal_id) REFERENCES animals_animal(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS animals_rescuerequestimage (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  rescue_request_id BIGINT NOT NULL,
  image VARCHAR(100) NOT NULL,
  sort_order INT UNSIGNED NOT NULL DEFAULT 0,
  INDEX rescue_image_request_idx (rescue_request_id),
  CONSTRAINT rescue_image_request_fk FOREIGN KEY (rescue_request_id) REFERENCES animals_rescuerequest(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
