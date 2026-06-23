'use client'

import { motion } from 'framer-motion'

interface StarDecorationProps {
  className?: string
  size?: number
  delay?: number
}

export default function StarDecoration({
  className = '',
  size = 32,
  delay = 0,
}: StarDecorationProps) {
  return (
    <motion.svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      className={className}
      initial={{ opacity: 0, scale: 0 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay, duration: 0.5, ease: 'easeOut' }}
    >
      <motion.path
        d="M16 0L19.5 12.5L32 16L19.5 19.5L16 32L12.5 19.5L0 16L12.5 12.5L16 0Z"
        fill="#FFA726"
        animate={{
          rotate: [0, 10, -10, 0],
          y: [0, -5, 0],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        style={{ transformOrigin: 'center' }}
      />
    </motion.svg>
  )
}
