'use client';
import React, { useEffect, useState } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from '@dnd-kit/core';
import {
  SortableContext,
  arrayMove,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { animated, useSpring } from 'react-spring';

interface ChannelSummaryCardsProps {
  data: Record<string, any>;
}

const defaultOrder = [
  'title',
  'id',
  'slug',
  'id_text',
  'podcast_guid',
  'medium_id',
  'has_value_time_splits',
];

const emojiLabels: Record<string, string> = {
  title: '💡 Title',
  id: '🆔 ID',
  slug: '🔗 Slug',
  id_text: '📝 ID Text',
  podcast_guid: '🎙️ Podcast GUID',
  medium_id: '📡 Medium ID',
  has_value_time_splits: '💰 Value Splits',
};

const Card = ({ id, label, value }: { id: string; label: string; value: any }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    zIndex: isDragging ? 50 : 1,
  };

  const spring = useSpring({
    opacity: isDragging ? 0.5 : 1,
    scale: isDragging ? 1.05 : 1,
    config: { tension: 300, friction: 20 },
  });

  return (
    <animated.div
      ref={setNodeRef}
      style={{ ...style, ...spring }}
      {...attributes}
      {...listeners}
      className={`bg-white dark:bg-gray-800 border border-blue-400 rounded-xl shadow p-4 w-full cursor-move select-none ${
        isDragging ? 'ring-2 ring-blue-500' : ''
      }`}
    >
      <p className="text-sm text-gray-400 dark:text-gray-500">{label}</p>
      <p className="text-base font-medium text-gray-900 dark:text-white truncate">
        {value !== null && value !== undefined ? value.toString() : <em className="text-gray-500">None</em>}
      </p>
    </animated.div>
  );
};

export default function ChannelSummaryCards({ data }: ChannelSummaryCardsProps) {
  const [cardOrder, setCardOrder] = useState<string[]>(defaultOrder);

  // Load saved layout
  useEffect(() => {
    const saved = localStorage.getItem('channelCardOrder');
    if (saved) setCardOrder(JSON.parse(saved));
  }, []);

  // Save layout on change
  useEffect(() => {
    localStorage.setItem('channelCardOrder', JSON.stringify(cardOrder));
  }, [cardOrder]);

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = ({ active, over }: DragEndEvent) => {
    if (!over || active.id === over.id) return;
    const oldIndex = cardOrder.indexOf(active.id as string);
    const newIndex = cardOrder.indexOf(over.id as string);
    setCardOrder(arrayMove(cardOrder, oldIndex, newIndex));
  };

  const handleReset = () => {
    setCardOrder(defaultOrder);
    localStorage.removeItem('channelCardOrder');
  };

  return (
    <div className="mb-6">
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-xl font-semibold">🧩 Channel Metadata</h2>
        <button
          onClick={handleReset}
          className="text-sm bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 transition"
        >
          Reset Order
        </button>
      </div>

      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={cardOrder} strategy={verticalListSortingStrategy}>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {cardOrder.map((key) => (
              <Card key={key} id={key} label={emojiLabels[key] || key} value={data[key]} />
            ))}
          </div>
        </SortableContext>
      </DndContext>
    </div>
  );
}
