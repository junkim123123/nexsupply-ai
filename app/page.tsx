import NavigationBar from '@/components/NavigationBar';
import HeroSection from '@/components/HeroSection';
import ValueProposition from '@/components/ValueProposition';
import CoreFeatures from '@/components/CoreFeatures';
import DashboardPreview from '@/components/DashboardPreview';
import SocialProof from '@/components/SocialProof';
import Pricing from '@/components/Pricing';
import Footer from '@/components/Footer';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-900 text-white">
      <NavigationBar />
      <HeroSection />
      <ValueProposition />
      <CoreFeatures />
      <DashboardPreview />
      <SocialProof />
      <Pricing />
      <Footer />
    </main>
  );
}
