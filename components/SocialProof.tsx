export default function SocialProof() {
  const logos = [
    'MAERSK',
    'Shopify',
    'Amazon',
    'JSF',
    'FORTUNE 500',
  ];

  return (
    <section className="bg-gray-900 py-16 border-y border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h3 className="text-2xl font-bold mb-2">Trusted by Global Leaders</h3>
          <p className="text-gray-400">Powering supply chains for the world's most innovative companies</p>
        </div>
        
        <div className="flex flex-wrap justify-center items-center gap-8 md:gap-12 opacity-60 hover:opacity-100 transition-opacity">
          {logos.map((logo, index) => (
            <div
              key={index}
              className="text-2xl font-bold text-gray-400 hover:text-white transition-colors cursor-pointer"
            >
              {logo}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

