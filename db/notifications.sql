CREATE TABLE IF NOT EXISTS notifications_notification (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  recipient_id BIGINT NOT NULL,
  business_type VARCHAR(20) NOT NULL DEFAULT 'system',
  title VARCHAR(100) NOT NULL,
  content LONGTEXT NOT NULL,
  related_app VARCHAR(50) NOT NULL DEFAULT '',
  related_object_id BIGINT UNSIGNED NULL,
  created_at DATETIME(6) NOT NULL,
  read_at DATETIME(6) NULL,
  INDEX notice_user_read_idx (recipient_id, read_at, created_at DESC),
  CONSTRAINT notifications_recipient_fk FOREIGN KEY (recipient_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
