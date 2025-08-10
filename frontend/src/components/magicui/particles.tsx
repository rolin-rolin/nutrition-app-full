"use client";

import { cn } from "@/lib/utils";
import React, { ComponentPropsWithoutRef, useCallback, useEffect, useRef, useState } from "react";

interface MousePosition {
    x: number;
    y: number;
}

function MousePosition(): MousePosition {
    const [mousePosition, setMousePosition] = useState<MousePosition>({
        x: 0,
        y: 0,
    });

    useEffect(() => {
        const handleMouseMove = (event: MouseEvent) => {
            setMousePosition({
                x: event.clientX,
                y: event.clientY,
            });
        };

        window.addEventListener("mousemove", handleMouseMove);

        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
        };
    }, []);

    return mousePosition;
}

interface ParticlesProps extends ComponentPropsWithoutRef<"div"> {
    className?: string;
    quantity?: number;
    staticity?: number;
    ease?: number;
    size?: number;
    refresh?: boolean;
    color?: string;
    vx?: number;
    vy?: number;
}

type Circle = {
    x: number;
    y: number;
    translateX: number;
    translateY: number;
    size: number;
    alpha: number;
    targetAlpha: number;
    dx: number;
    dy: number;
    magnetism: number;
};

export const Particles: React.FC<ParticlesProps> = ({
    className = "",
    quantity = 100,
    staticity = 50,
    ease = 50,
    size = 0.4,
    refresh = false,
    color = "#ffffff",
    vx = 0,
    vy = 0,
    ...props
}) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const canvasContainerRef = useRef<HTMLDivElement>(null);
    const context = useRef<CanvasRenderingContext2D | null>(null);
    const circles = useRef<Circle[]>([]);
    const mousePosition = MousePosition();
    const mouse = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
    const canvasSize = useRef<{ w: number; h: number }>({ w: 0, h: 0 });
    const dpr = typeof window !== "undefined" ? window.devicePixelRatio : 1;
    const rafID = useRef<number | null>(null);
    const resizeTimeout = useRef<NodeJS.Timeout | null>(null);

    const clearContext = useCallback(() => {
        if (context.current) {
            context.current.clearRect(0, 0, canvasSize.current.w, canvasSize.current.h);
        }
    }, []);

    const circleParams = useCallback((): Circle => {
        const canvas = canvasSize.current;
        const circle = {
            x: Math.random() * canvas.w,
            y: Math.random() * canvas.h,
            translateX: 0,
            translateY: 0,
            size: size,
            alpha: 0,
            targetAlpha: parseFloat((Math.random() * 0.6 + 0.1).toFixed(1)),
            dx: parseFloat((Math.random() * 2 - 1).toFixed(2)),
            dy: parseFloat((Math.random() * 2 - 1).toFixed(2)),
            magnetism: parseFloat((Math.random() * 0.2 + 0.6).toFixed(2)),
        };
        return circle;
    }, [size]);

    const drawCircle = useCallback(
        (circle: Circle, update = false) => {
            if (context.current) {
                context.current.save();
                context.current.globalAlpha = circle.alpha;
                context.current.fillStyle = color;
                context.current.beginPath();
                context.current.arc(
                    circle.x + circle.translateX,
                    circle.y + circle.translateY,
                    circle.size,
                    0,
                    2 * Math.PI
                );
                context.current.fill();
                context.current.restore();
                if (!update) {
                    circles.current.push(circle);
                }
            }
        },
        [color]
    );

    const drawParticles = useCallback(() => {
        clearContext();
        const particleCount = quantity;
        for (let i = 0; i < particleCount; i++) {
            const circle = circleParams();
            drawCircle(circle);
        }
    }, [clearContext, quantity, circleParams, drawCircle]);

    const resizeCanvas = useCallback(() => {
        if (canvasContainerRef.current && canvasRef.current && context.current) {
            canvasSize.current.w = canvasContainerRef.current.offsetWidth;
            canvasSize.current.h = canvasContainerRef.current.offsetHeight;

            canvasRef.current.width = canvasSize.current.w * dpr;
            canvasRef.current.height = canvasSize.current.h * dpr;
            canvasRef.current.style.width = `${canvasSize.current.w}px`;
            canvasRef.current.style.height = `${canvasSize.current.h}px`;
            context.current.scale(dpr, dpr);

            // Clear existing particles and create new ones with exact quantity
            circles.current = [];
            for (let i = 0; i < quantity; i++) {
                const circle = circleParams();
                drawCircle(circle);
            }
        }
    }, [dpr, quantity, circleParams, drawCircle]);

    const initCanvas = useCallback(() => {
        resizeCanvas();
        drawParticles();
    }, [resizeCanvas, drawParticles]);

    const onMouseMove = useCallback(() => {
        if (canvasRef.current) {
            const rect = canvasRef.current.getBoundingClientRect();
            const { w, h } = canvasSize.current;
            const x = mousePosition.x - rect.left - w / 2;
            const y = mousePosition.y - rect.top - h / 2;
            const inside = x < w / 2 && x > -w / 2 && y < h / 2 && y > -h / 2;
            if (inside) {
                mouse.current.x = x;
                mouse.current.y = y;
            }
        }
    }, [mousePosition.x, mousePosition.y]);

    const animate = useCallback(() => {
        clearContext();
        circles.current.forEach((circle: Circle, i: number) => {
            // Handle the alpha value
            const edge = [
                circle.x + circle.translateX - circle.size, // distance from left edge
                canvasSize.current.w - circle.x - circle.translateX - circle.size, // distance from right edge
                circle.y + circle.translateY - circle.size, // distance from top edge
                canvasSize.current.h - circle.y + circle.translateY - circle.size, // distance from bottom edge
            ];
            const closestEdge = edge.reduce((a, b) => Math.min(a, b));
            const remapClosestEdge = parseFloat(remapValue(closestEdge, 0, 20, 0, 1).toFixed(2));
            if (remapClosestEdge > 1) {
                circle.alpha += 0.02;
                if (circle.alpha > circle.targetAlpha) {
                    circle.alpha = circle.targetAlpha;
                }
            } else {
                circle.alpha = circle.targetAlpha * remapClosestEdge;
            }
            circle.x += circle.dx + vx;
            circle.y += circle.dy + vy;
            circle.translateX += (mouse.current.x / (staticity / circle.magnetism) - circle.translateX) / ease;
            circle.translateY += (mouse.current.y / (staticity / circle.magnetism) - circle.translateY) / ease;

            drawCircle(circle, true);

            // circle gets out of the canvas
            if (
                circle.x < -circle.size ||
                circle.x > canvasSize.current.w + circle.size ||
                circle.y < -circle.size ||
                circle.y > canvasSize.current.h + circle.size
            ) {
                // remove the circle from the array
                circles.current.splice(i, 1);
                // create a new circle
                const newCircle = circleParams();
                drawCircle(newCircle);
            }
        });
        rafID.current = window.requestAnimationFrame(animate);
    }, [vx, vy, staticity, ease, clearContext, circleParams, drawCircle]);

    useEffect(() => {
        if (canvasRef.current) {
            context.current = canvasRef.current.getContext("2d");
        }
        initCanvas();
        animate();

        const handleResize = () => {
            if (resizeTimeout.current) {
                clearTimeout(resizeTimeout.current);
            }
            resizeTimeout.current = setTimeout(() => {
                initCanvas();
            }, 200);
        };

        window.addEventListener("resize", handleResize);

        return () => {
            if (rafID.current != null) {
                window.cancelAnimationFrame(rafID.current);
            }
            if (resizeTimeout.current) {
                clearTimeout(resizeTimeout.current);
            }
            window.removeEventListener("resize", handleResize);
        };
    }, [color, initCanvas, animate]);

    useEffect(() => {
        onMouseMove();
    }, [onMouseMove]);

    useEffect(() => {
        initCanvas();
    }, [refresh, initCanvas]);

    const remapValue = (value: number, start1: number, end1: number, start2: number, end2: number): number => {
        const remapped = ((value - start1) * (end2 - start2)) / (end1 - start1) + start2;
        return remapped > 0 ? remapped : 0;
    };

    return (
        <div className={cn("pointer-events-none", className)} ref={canvasContainerRef} aria-hidden="true" {...props}>
            <canvas ref={canvasRef} className="size-full" />
        </div>
    );
};
