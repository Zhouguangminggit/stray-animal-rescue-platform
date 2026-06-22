CREATE TABLE IF NOT EXISTS adoptions_adoptionapplication (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  applicant_id BIGINT NOT NULL,
  animal_id BIGINT NOT NULL,
  motivation LONGTEXT NOT NULL,
  housing VARCHAR(255) NOT NULL,
  experience LONGTEXT NOT NULL,
  contact VARCHAR(100) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  pending_marker BOOLEAN NULL DEFAULT TRUE,
  review_note LONGTEXT NOT NULL,
  reviewed_by_id BIGINT NULL,
  reviewed_at DATETIME(6) NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  CONSTRAINT uniq_pending_adoption_user_animal UNIQUE (applicant_id, animal_id, pending_marker),
  INDEX adoption_review_idx (status, created_at DESC),
  CONSTRAINT adoption_application_user_fk FOREIGN KEY (applicant_id) REFERENCES accounts_user(id),
  CONSTRAINT adoption_application_animal_fk FOREIGN KEY (animal_id) REFERENCES animals_animal(id),
  CONSTRAINT adoption_application_reviewer_fk FOREIGN KEY (reviewed_by_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS adoptions_adoptionrelationship (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  application_id BIGINT NOT NULL UNIQUE,
  adopter_id BIGINT NOT NULL,
  animal_id BIGINT NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  active_marker BOOLEAN NULL DEFAULT TRUE,
  started_at DATETIME(6) NOT NULL,
  ended_at DATETIME(6) NULL,
  end_note LONGTEXT NOT NULL,
  created_at DATETIME(6) NOT NULL,
  CONSTRAINT uniq_active_adoption_animal UNIQUE (animal_id, active_marker),
  INDEX adoption_user_status_idx (adopter_id, status),
  CONSTRAINT adoption_relationship_application_fk FOREIGN KEY (application_id) REFERENCES adoptions_adoptionapplication(id),
  CONSTRAINT adoption_relationship_user_fk FOREIGN KEY (adopter_id) REFERENCES accounts_user(id),
  CONSTRAINT adoption_relationship_animal_fk FOREIGN KEY (animal_id) REFERENCES animals_animal(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
