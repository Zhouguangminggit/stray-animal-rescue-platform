import Navbar from '@/sections/Navbar'
import HeroSection from '@/sections/HeroSection'
import AboutSection from '@/sections/AboutSection'
import ServicesSection from '@/sections/ServicesSection'
import PetsSection from '@/sections/PetsSection'
import GetInvolvedSection from '@/sections/GetInvolvedSection'
import StatsSection from '@/sections/StatsSection'
import ContactSection from '@/sections/ContactSection'
import Footer from '@/sections/Footer'

function App() {
  return (
    <div className="min-h-screen bg-warm-white">
      <Navbar />
      <main>
        <HeroSection />
        <AboutSection />
        <ServicesSection />
        <PetsSection />
        <GetInvolvedSection />
        <StatsSection />
        <ContactSection />
      </main>
      <Footer />
    </div>
  )
}

export default App
