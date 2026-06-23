'use client'

import { useRef } from 'react'
import AnimatedSection from '@/components/AnimatedSection'
import PetCard from '@/components/PetCard'
import { ChevronLeft, ChevronRight } from 'lucide-react'

const pets = [
  {
    name: '豆豆',
    age: '2岁',
    breed: '金毛混血',
    description: '性格温顺，喜欢和孩子玩耍',
    image: '/images/pet-doudou.jpg',
  },
  {
    name: '花花',
    age: '1岁',
    breed: '橘猫',
    description: '活泼好动，超级亲人',
    image: '/images/pet-huahua.jpg',
  },
  {
    name: '小黑',
    age: '3岁',
    breed: '拉布拉多',
    description: '忠诚可靠，训练有素',
    image: '/images/pet-xiaohei.jpg',
  },
  {
    name: '咪咪',
    age: '6个月',
    breed: '三花猫',
    description: '软萌可爱，喜欢撒娇',
    image: '/images/pet-mimi.jpg',
  },
  {
    name: '旺财',
    age: '4岁',
    breed: '柴犬混血',
    description: '精力充沛，热爱户外运动',
    image: '/images/pet-wangcai.jpg',
  },
  {
    name: '雪球',
    age: '1岁',
    breed: '白猫',
    description: '安静优雅，适合安静的家庭',
    image: '/images/pet-xueqiu.jpg',
  },
]

export default function PetsSection() {
  const scrollRef = useRef<HTMLDivElement>(null)

  const scroll = (direction: 'left' | 'right') => {
    if (scrollRef.current) {
      const scrollAmount = 304 // card width + gap
      scrollRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth',
      })
    }
  }

  return (
    <section id="pets" className="py-20 md:py-28 lg:py-32 bg-light-orange">
      <div className="max-w-7xl mx-auto px-5 md:px-10 lg:px-20">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end md:justify-between mb-10 md:mb-12">
          <div>
            <AnimatedSection>
              <span className="inline-block font-label text-lg md:text-xl text-primary bg-white/60 px-4 py-1.5 rounded-full -rotate-2 mb-4">
                寻找家人
              </span>
            </AnimatedSection>
            <AnimatedSection delay={0.1}>
              <h2 className="font-display text-3xl md:text-4xl lg:text-5xl text-gradient">
                等待回家的
                <br className="hidden sm:block" />
                小伙伴们
              </h2>
            </AnimatedSection>
          </div>

          {/* Scroll Buttons */}
          <AnimatedSection delay={0.2}>
            <div className="flex gap-3 mt-6 md:mt-0">
              <button
                onClick={() => scroll('left')}
                className="w-12 h-12 rounded-full bg-white shadow-md flex items-center justify-center text-primary hover:bg-primary hover:text-white transition-all duration-200"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              <button
                onClick={() => scroll('right')}
                className="w-12 h-12 rounded-full bg-white shadow-md flex items-center justify-center text-primary hover:bg-primary hover:text-white transition-all duration-200"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </AnimatedSection>
        </div>

        {/* Pets Scroll Container */}
        <div
          ref={scrollRef}
          className="flex gap-6 overflow-x-auto scrollbar-hide pb-4 snap-x snap-mandatory"
        >
          {pets.map((pet, index) => (
            <div key={index} className="snap-start">
              <PetCard
                name={pet.name}
                age={pet.age}
                breed={pet.breed}
                description={pet.description}
                image={pet.image}
                delay={index * 0.1}
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
