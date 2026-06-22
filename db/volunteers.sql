CREATE TABLE IF NOT EXISTS volunteers_volunteerapplication (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, applicant_id BIGINT NOT NULL,
  intention LONGTEXT NOT NULL, skills VARCHAR(255) NOT NULL,
  availability VARCHAR(255) NOT NULL, experience LONGTEXT NOT NULL,
  material VARCHAR(100) NOT NULL DEFAULT '', status VARCHAR(20) NOT NULL DEFAULT 'pending',
  review_note LONGTEXT NOT NULL, reviewed_by_id BIGINT NULL, reviewed_at DATETIME(6) NULL,
  created_at DATETIME(6) NOT NULL, updated_at DATETIME(6) NOT NULL,
  INDEX volunteer_review_idx (status, created_at DESC),
  CONSTRAINT volunteer_application_user_fk FOREIGN KEY (applicant_id) REFERENCES accounts_user(id),
  CONSTRAINT volunteer_application_reviewer_fk FOREIGN KEY (reviewed_by_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS volunteers_volunteerprofile (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT NOT NULL UNIQUE,
  source_application_id BIGINT NULL UNIQUE, skills VARCHAR(255) NOT NULL,
  availability VARCHAR(255) NOT NULL, bio LONGTEXT NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active', joined_at DATETIME(6) NOT NULL,
  CONSTRAINT volunteer_profile_user_fk FOREIGN KEY (user_id) REFERENCES accounts_user(id),
  CONSTRAINT volunteer_profile_application_fk FOREIGN KEY (source_application_id) REFERENCES volunteers_volunteerapplication(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS volunteers_volunteerprofile_tags (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, volunteerprofile_id BIGINT NOT NULL, tag_id BIGINT NOT NULL,
  UNIQUE KEY volunteer_profile_tag_unique (volunteerprofile_id, tag_id),
  CONSTRAINT volunteer_profile_tags_profile_fk FOREIGN KEY (volunteerprofile_id) REFERENCES volunteers_volunteerprofile(id),
  CONSTRAINT volunteer_profile_tags_tag_fk FOREIGN KEY (tag_id) REFERENCES tags_tag(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS volunteers_communityarticle (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(150) NOT NULL,
  summary VARCHAR(300) NOT NULL, content LONGTEXT NOT NULL, cover VARCHAR(100) NOT NULL DEFAULT '',
  is_published BOOLEAN NOT NULL DEFAULT TRUE, published_at DATETIME(6) NULL,
  created_at DATETIME(6) NOT NULL, updated_at DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS volunteers_communityarticle_tags (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, communityarticle_id BIGINT NOT NULL, tag_id BIGINT NOT NULL,
  UNIQUE KEY community_article_tag_unique (communityarticle_id, tag_id),
  CONSTRAINT community_article_tags_article_fk FOREIGN KEY (communityarticle_id) REFERENCES volunteers_communityarticle(id),
  CONSTRAINT community_article_tags_tag_fk FOREIGN KEY (tag_id) REFERENCES tags_tag(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS volunteers_communitypost (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, author_id BIGINT NOT NULL,
  title VARCHAR(150) NOT NULL, content LONGTEXT NOT NULL, is_hidden BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME(6) NOT NULL, updated_at DATETIME(6) NOT NULL,
  INDEX community_post_pub_idx (is_hidden, created_at DESC),
  CONSTRAINT community_post_author_fk FOREIGN KEY (author_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS volunteers_communityreport (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, reporter_id BIGINT NOT NULL, post_id BIGINT NOT NULL,
  reason LONGTEXT NOT NULL, status VARCHAR(20) NOT NULL DEFAULT 'pending', pending_marker BOOLEAN NULL DEFAULT TRUE,
  resolution_note LONGTEXT NOT NULL, reviewed_by_id BIGINT NULL, reviewed_at DATETIME(6) NULL,
  created_at DATETIME(6) NOT NULL,
  CONSTRAINT uniq_pending_reporter_post UNIQUE (reporter_id, post_id, pending_marker),
  CONSTRAINT community_report_user_fk FOREIGN KEY (reporter_id) REFERENCES accounts_user(id),
  CONSTRAINT community_report_post_fk FOREIGN KEY (post_id) REFERENCES volunteers_communitypost(id),
  CONSTRAINT community_report_reviewer_fk FOREIGN KEY (reviewed_by_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
