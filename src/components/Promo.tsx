import { useScroll, useTransform, motion } from "framer-motion";
import { useRef } from "react";

export default function Promo() {
  const container = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: container,
    offset: ["start end", "end start"],
  });
  const y = useTransform(scrollYProgress, [0, 1], ["-10vh", "10vh"]);

  return (
    <div
      ref={container}
      className="relative flex items-center justify-center h-screen overflow-hidden"
      style={{ clipPath: "polygon(0% 0, 100% 0%, 100% 100%, 0 100%)" }}
    >
      <div className="fixed top-[-10vh] left-0 h-[120vh] w-full">
        <motion.div style={{ y }} className="relative w-full h-full">
          <img
            src="/images/spiral-circles.jpg"
            alt="Abstract spiral circles"
            className="w-full h-full object-cover"
          />
        </motion.div>
      </div>

      <h3 id="pricing" className="absolute top-12 right-6 text-white uppercase z-10 text-sm md:text-base lg:text-lg">
        Тарифы
      </h3>

      <div className="absolute bottom-12 left-6 right-6 z-10 flex flex-col sm:flex-row gap-6 sm:gap-8 items-start sm:items-end">
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 sm:p-8 flex-1 max-w-sm">
          <h4 className="text-white text-lg uppercase tracking-wide mb-2">VIP</h4>
          <p className="text-white text-4xl sm:text-5xl font-bold mb-2">10 ₽</p>
          <p className="text-white/70 text-sm mb-4">Расширенная команда и базовые ресурсы для старта</p>
          <button className="bg-white text-black px-6 py-2 text-sm uppercase tracking-wide font-semibold hover:bg-neutral-200 transition-colors duration-300 w-full">
            Подключить
          </button>
        </div>
        <div className="bg-white/15 backdrop-blur-md border border-white/30 rounded-2xl p-6 sm:p-8 flex-1 max-w-sm">
          <h4 className="text-white text-lg uppercase tracking-wide mb-2">Премиум</h4>
          <p className="text-white text-4xl sm:text-5xl font-bold mb-2">50 ₽</p>
          <p className="text-white/70 text-sm mb-4">Максимум ресурсов, большая команда, приоритетная поддержка</p>
          <button className="bg-white text-black px-6 py-2 text-sm uppercase tracking-wide font-semibold hover:bg-neutral-200 transition-colors duration-300 w-full">
            Подключить
          </button>
        </div>
      </div>
    </div>
  );
}